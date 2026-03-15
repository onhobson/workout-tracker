import pytest

from fastapi.testclient import TestClient

from app.core.limits import USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH


def create_user(client: TestClient, username="username", email="user@example.com", password="12345"):
    return client.post(
        "/users",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


class TestCreateUser:
    def test_create_user(self, client: TestClient):
        response = create_user(client)

        assert response.status_code == 201

        data = response.json()

        assert data["username"] == "username"
        assert data["email"] == "user@example.com"

    
    @pytest.mark.parametrize(
            "username,email",
            [
                ("username", "otheremail@example.com"),
                ("newname", "user@example.com"),
            ]
    )
    def test_create_user_unique_values(self, client: TestClient, username, email):
        create_user(client)
        response = create_user(client, username=username, email=email)

        assert response.status_code == 422

    
    @pytest.mark.parametrize(
            "username,email,password",
            [
                ("", "user1@example.com", "12345"),
                ("     ", "user2@example.com", "12345"),
                ("user3", "", "12345"),
                ("user4", "     ", "12345"),
                ("user5", "user5@example.com", ""),
                ("user6", "user6@example.com", "   "),
            ]
    )
    def test_create_user_invalid_values(self, client: TestClient, username, email, password):
        response = create_user(client, username, email, password)

        assert response.status_code == 422

    
    def test_create_user_username_max_length(self, client: TestClient):
        a_very_long_name = "a" * (USERNAME_MAX_LENGTH + 1)
        response = create_user(client, username=a_very_long_name)

        assert response.status_code == 422

    
    def test_create_user_email_max_length(self, client: TestClient):
        a_very_long_email = "a" * (EMAIL_MAX_LENGTH + 1) + "@example.com"
        response = create_user(client, email=a_very_long_email)

        assert response.status_code == 422


class TestUserLogin:
    def test_login(self, client: TestClient):
        create_user(client, username="username", password="12345")

        response = client.post(
            "/auth/login",
            data={
                "username": "username",
                "password": "12345"
            }
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["access_token"] is not None
        assert response_data["token_type"] == "bearer"

    
    def test_login_invalid_username(self, client: TestClient):
        create_user(client, username="username", password="12345")

        response = client.post(
            "/auth/login",
            data={
                "username": "badusername",
                "password": "12345"
            }
        )

        assert response.status_code == 401

    
    def test_login_invalid_password(self, client: TestClient):
        create_user(client, username="username", password="12345")

        response = client.post(
            "/auth/login",
            data={
                "username": "username",
                "password": "badpassword"
            }
        )

        assert response.status_code == 401


class TestReadUser:
    def test_get_user(self, auth_client: TestClient):
        response = auth_client.get(
            "/users"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["id"] == 1

    
    def test_get_user_unauth(self, client: TestClient):
        response = client.get(
            "/users"
        )

        assert response.status_code == 401


class TestUpdateUser:
    def test_update_user(self, auth_client: TestClient):
        response = auth_client.put(
            "/users",
            json={
                "username": "newname",
                "email": "new@example.com"
            }
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["username"] == "newname"
        assert response_data["email"] == "new@example.com"

    
    @pytest.mark.parametrize(
        "username,email",
        [
            ("", "test@example.com"),
            ("  ", "test@example.com"),
            ("username", ""),
            ("username", "   ")
        ]
    )
    def test_update_user_invalid(self, auth_client: TestClient, username, email):
        response = auth_client.put(
            "/users",
            json={
                "username": username,
                "email": email
            }
        )

        assert response.status_code == 422

    
    def test_update_user_unauth(self, client: TestClient):
        response = client.get(
            "/users"
        )

        assert response.status_code == 401

    
    def test_update_user_password(self, auth_client: TestClient):
        auth_client.put(
            "/users",
            json={
                "password": "newpassword098"
            }
        )

        response = auth_client.post(
            "/auth/login",
            data={
                "username": "testuser",
                "password": "newpassword098"
            }
        )

        assert response.status_code == 200


    def test_update_user_username_max_length(self, auth_client: TestClient):
        a_very_long_name = "a" * (USERNAME_MAX_LENGTH + 1)
        response = auth_client.put(
            "/users",
            json={
                "username": a_very_long_name
            }
        )

        assert response.status_code == 422

    
    def test_update_user_email_length(self, auth_client: TestClient):
        a_very_long_email = "a" * (EMAIL_MAX_LENGTH + 1) + "@example.com"
        response = auth_client.put(
            "/users",
            json={
                "email": a_very_long_email
            }
        )

        assert response.status_code == 422


class TestDeleteUser:
    def test_delete_user(self, auth_client: TestClient):
        response = auth_client.delete(
            "/users"
        )

        assert response.status_code == 204

    
    def test_delete_user_unauth(self, client: TestClient):
        response = client.delete(
            "/users"
        )

        assert response.status_code == 401