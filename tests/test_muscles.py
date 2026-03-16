from fastapi.testclient import TestClient

from tests.factories import muscle_factory

MU_DATA = [
    ("Chest", True),
    ("Back", True),
    ("Adductors", False)
]

def seed_mu_data(client: TestClient, muscle_factory):
    for name, is_primary in MU_DATA:
        muscle_factory(name=name, is_primary=is_primary)


def test_get_all_muscle_groups(client: TestClient, muscle_factory):
    seed_mu_data(client, muscle_factory)

    response = client.get(
        "/muscles"
    )

    assert response.status_code == 200

    response_data = response.json()

    for i, data in enumerate(MU_DATA):
        assert response_data[i]["id"] == i + 1
        assert response_data[i]["name"] == data[0]
        assert response_data[i]["is_primary"] == data[1]


def test_get_muscle_group(client: TestClient, muscle_factory):
    seed_mu_data(client, muscle_factory)

    for i, data in enumerate(MU_DATA):
        response = client.get(
            f"/muscles/{i + 1}"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["id"] == i + 1
        assert response_data["name"] == data[0]
        assert response_data["is_primary"] == data[1]


def test_get_muscle_group_invalid_id(client: TestClient, muscle_factory):
    seed_mu_data(client, muscle_factory)

    response = client.get(
        "/muscles/20"
    )

    assert response.status_code == 404