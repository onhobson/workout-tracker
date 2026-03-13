import pytest

from fastapi.testclient import TestClient


def create_user(client: TestClient, username="testuser"):
    return client.post(
        "/users",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "password"
        }
    )
    

class TestCreateUser:

    def test_create_user(self, client: TestClient):
        response = create_user(client)

        assert response.status_code == 201

        data = response.json()

        assert data["username"] == "testuser"
        assert data["email"] == "testuser@example.com"

    
    def test_create_duplicate_user(self, client: TestClient):
        create_user(client)
        response = create_user(client)
        assert response.status_code == 400

    
    @pytest.mark.parametrize(
            "username,email,password",
            [
                ("", "test@example.com", "password"),
                ("username", "", "password"),
                ("username", "bademail", "password"),
                ("username", "test@example.com", ""),
            ]
    )
    def test_create_user_invalid_input(self, client: TestClient, username, email, password):
        response = client.post(
            "/users",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 422

        