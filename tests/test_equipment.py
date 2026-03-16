from fastapi.testclient import TestClient

from tests.factories import equipment_factory


EQ_DATA = [
    ("Barbell", "barbell"),
    ("Dumbbell", "double"),
    ("Cable", "single")
]


def seed_eq_data(client: TestClient, equipment_factory):
    for name, input in EQ_DATA:
        equipment_factory(name=name, input_mode=input)


def test_get_all_equipment(client: TestClient, equipment_factory):
    seed_eq_data(client, equipment_factory)

    response = client.get(
        "/equipment"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 3

    for i, data in enumerate(EQ_DATA):
        assert response_data[i]["id"] == i + 1
        assert response_data[i]["name"] == data[0]
        assert response_data[i]["input_mode"] == data[1]


def test_get_equipment(client: TestClient, equipment_factory):
    seed_eq_data(client, equipment_factory)

    for i, data in enumerate(EQ_DATA):
        response = client.get(
            f"/equipment/{i + 1}"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["name"] == data[0]
        assert response_data["input_mode"] == data[1]


def test_get_equipment_invalid_id(client: TestClient, equipment_factory):
    seed_eq_data(client, equipment_factory)

    response = client.get(
        "/equipment/10"
    )

    assert response.status_code == 404