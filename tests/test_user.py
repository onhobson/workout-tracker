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

