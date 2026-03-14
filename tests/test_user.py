import pytest

from fastapi.testclient import TestClient


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
