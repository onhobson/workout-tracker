import pytest

from fastapi.testclient import TestClient

from tests.factories import exercise_factory, equipment_factory, muscle_factory

EX_DATA = [
    (1, "Barbell", "Bench Press", [("Chest", "primary"), ("Triceps", "secondary")]),
    (2, "Dumbbell", "Shoulder Press", [("Shoulders", "primary")]),
    (3, "Bodyweight", "Pull Ups", [("Lats", "primary"), ("Biceps", "secondary")])
]

@pytest.fixture()
def seed_ex_data(exercise_factory, equipment_factory, muscle_factory):
    
    def seed(ex_data: list[tuple]):
        exercises = []
        for _, eq, name, muscles in ex_data:
            equipment = equipment_factory(name=eq)

            muscle_list = []
            for muscle in muscles:
                # Appends tuples in form (id, role)
                muscle_list.append((muscle_factory(name=muscle[0]).id, muscle[1]))

            exercises.append(
                exercise_factory(
                    muscles=[(id, role) for id, role in muscle_list],
                    equipment_id=equipment.id,
                    name=name
                )
            )
        
        return exercises
    
    return seed

class TestReadExercises():
    def test_get_exercises(self, auth_client: TestClient, seed_ex_data):
        exercises = seed_ex_data(EX_DATA)

        response = auth_client.get(
            "/exercises"
        )

        assert response.status_code == 200

        response_data = response.json()

        for i, exercise in enumerate(exercises):
            assert response_data[i]["id"] == exercise.id
            assert response_data[i]["equipment"]["id"] == exercise.equipment_id
            
            for j, muscle in enumerate(exercise.muscles):
                assert response_data[i]["muscles"][j]["muscle"]["id"] == muscle.muscle_group_id
                assert response_data[i]["muscles"][j]["role"] == muscle.role

    
    def test_get_exercise(self, auth_client: TestClient, seed_ex_data):
        exercises = seed_ex_data(EX_DATA)

        for exercise in exercises:
            response = auth_client.get(
                f"/exercises/{exercise.id}"
            )

            assert response.status_code == 200

            response_data = response.json()

            assert response_data["id"] == exercise.id
            assert response_data["equipment"]["id"] == exercise.equipment_id
            
            for i, muscle in enumerate(exercise.muscles):
                assert response_data["muscles"][i]["muscle"]["id"] == muscle.muscle_group_id
                assert response_data["muscles"][i]["role"] == muscle.role

    
    def test_get_exercise_invalid_id(self, auth_client: TestClient, seed_ex_data):
        seed_ex_data(EX_DATA)

        response = auth_client.get(
            "/exercises/20"
        )

        assert response.status_code == 404


    def test_get_exercises_with_filters(self, auth_client: TestClient, seed_ex_data):
        seed_ex_data(EX_DATA)

        response = auth_client.get(
            "/exercises?muscle_id=1&equipment_id=1"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == 1
        assert response_data[0]["id"] == 1


    def test_get_exercises_with_one_filter(self, auth_client: TestClient, seed_ex_data):
        seed_ex_data(EX_DATA)

        response = auth_client.get(
            "/exercises?muscle_id=1"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == 1

        response = auth_client.get(
            "/exercises?equipment_id=1"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == 1

    
    def test_get_exercises_with_filters_no_results(self, auth_client: TestClient, seed_ex_data):
        seed_ex_data(EX_DATA)

        response = auth_client.get(
            "/exercises?muscle_id=1&equipment_id=2"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == 0


    def test_get_exercises_with_invalid_filters(self, auth_client: TestClient, seed_ex_data):
        seed_ex_data(EX_DATA)

        response = auth_client.get(
            "/exercises?muscle_id=20&equipment_id=20"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == 0


    def test_get_exercises_with_user_created_exercises(self, auth_client: TestClient, seed_ex_data, exercise_factory):
        exercises = seed_ex_data(EX_DATA)

        exercise_factory(
            name="User Created Exercise",
            equipment_id=exercises[0].equipment_id,
            created_by_user_id=1
        )

        response = auth_client.get(
            "/exercises"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == len(exercises) + 1

    
    def test_get_exercises_does_not_return_other_users_exercises(self, auth_client: TestClient, seed_ex_data, exercise_factory):
        exercises = seed_ex_data(EX_DATA)

        exercise_factory(
            name="Other User's Exercise",
            equipment_id=exercises[0].equipment_id,
            created_by_user_id=2
        )

        response = auth_client.get(
            "/exercises"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == len(exercises)

    def test_get_exercise_returns_user_created_exercise(self, auth_client: TestClient, seed_ex_data, exercise_factory):
        exercises = seed_ex_data(EX_DATA)

        user_exercise = exercise_factory(
            name="User Created Exercise",
            equipment_id=exercises[0].equipment_id,
            created_by_user_id=1
        )

        response = auth_client.get(
            f"/exercises/{user_exercise.id}"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["id"] == user_exercise.id
        assert response_data["equipment"]["id"] == user_exercise.equipment_id


    def test_get_exercise_does_not_return_other_users_exercise(self, auth_client: TestClient, seed_ex_data, exercise_factory):
        exercises = seed_ex_data(EX_DATA)

        other_exercise = exercise_factory(
            name="Other User's Exercise",
            equipment_id=exercises[0].equipment_id,
            created_by_user_id=2
        )

        response = auth_client.get(
            f"/exercises/{other_exercise.id}"
        )

        assert response.status_code == 404


    def test_get_exercises_no_exercises(self, auth_client: TestClient):
        response = auth_client.get(
            "/exercises"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == 0


    def test_get_exercise_no_exercises(self, auth_client: TestClient):
        response = auth_client.get(
            "/exercises/1"
        )

        assert response.status_code == 404


class TestCreateExercise():
    def test_create_exercise(self, auth_client: TestClient, equipment_factory, muscle_factory):
        equipment = equipment_factory(name="Barbell")

        muscle_1 = muscle_factory(name="Chest")
        muscle_2 = muscle_factory(name="Triceps")

        response = auth_client.post(
            "/exercises",
            json={
                "name": "Bench Press",
                "equipment_id": equipment.id,
                "muscle_groups": [
                    {"muscle_group_id": muscle_1.id, "role": "primary"},
                    {"muscle_group_id": muscle_2.id, "role": "secondary"}
                ]
            }
        )

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["name"] == "Bench Press"
        assert response_data["equipment"]["id"] == equipment.id

        for i, muscle in enumerate(response_data["muscles"]):
            assert muscle["muscle"]["id"] == (muscle_1.id if i == 0 else muscle_2.id)
            assert muscle["role"] == ("primary" if i == 0 else "secondary")


    def test_create_exercise_empty_name(self, auth_client: TestClient, equipment_factory, muscle_factory):
        equipment = equipment_factory(name="Barbell")

        muscle = muscle_factory(name="Chest")

        response = auth_client.post(
            "/exercises",
            json={
                "name": "",
                "equipment_id": equipment.id,
                "muscle_groups": [
                    {"muscle_group_id": muscle.id, "role": "primary"}
                ]
            }
        )

        assert response.status_code == 422


    def test_create_exercise_invalid_equipment_id(self, auth_client: TestClient, muscle_factory):
        muscle = muscle_factory(name="Chest")

        response = auth_client.post(
            "/exercises",
            json={
                "name": "Bench Press",
                "equipment_id": 20,
                "muscle_groups": [
                    {"muscle_group_id": muscle.id, "role": "primary"}
                ]
            }
        )

        assert response.status_code == 404

        assert response.json()["detail"] == "Given equipment_id: 20 not found"


    def test_create_exercise_invalid_muscle_group_id(self, auth_client: TestClient, equipment_factory):
        equipment = equipment_factory(name="Barbell")

        response = auth_client.post(
            "/exercises",
            json={
                "name": "Bench Press",
                "equipment_id": equipment.id,
                "muscle_groups": [
                    {"muscle_group_id": 20, "role": "primary"}
                ]
            }
        )

        assert response.status_code == 404

        assert response.json()["detail"] == "Given muscle_group_id: 20 not found"

    
    def test_create_exercise_muscle_group_empty_role(self, auth_client: TestClient, equipment_factory, muscle_factory):
        equipment = equipment_factory(name="Barbell")

        muscle = muscle_factory(name="Chest")

        response = auth_client.post(
            "/exercises",
            json={
                "name": "Bench Press",
                "equipment_id": equipment.id,
                "muscle_groups": [
                    {"muscle_group_id": muscle.id, "role": ""}
                ]
            }
        )

        assert response.status_code == 422

        assert response.json()["detail"][0]["type"] == "enum"


    def test_create_exercise_muscle_group_role_whitespace(self, auth_client: TestClient, equipment_factory, muscle_factory):
        equipment = equipment_factory(name="Barbell")

        muscle = muscle_factory(name="Chest")

        response = auth_client.post(
            "/exercises",
            json={
                "name": "Bench Press",
                "equipment_id": equipment.id,
                "muscle_groups": [
                    {"muscle_group_id": muscle.id, "role": "   "}
                ]
            }
        )

        assert response.status_code == 422

        assert response.json()["detail"][0]["type"] == "enum"

    
    def test_create_exercise_no_muscle_groups(self, auth_client: TestClient, equipment_factory):
        equipment = equipment_factory(name="Barbell")

        response = auth_client.post(
            "/exercises",
            json={
                "name": "Bench Press",
                "equipment_id": equipment.id,
                "muscle_groups": []
            }
        )

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["name"] == "Bench Press"
        assert response_data["equipment"]["id"] == equipment.id
        assert len(response_data["muscles"]) == 0


    def test_create_exercise_name_whitespace(self, auth_client: TestClient, equipment_factory, muscle_factory):
        equipment = equipment_factory(name="Barbell")

        muscle = muscle_factory(name="Chest")

        response = auth_client.post(
            "/exercises",
            json={
                "name": "   ",
                "equipment_id": equipment.id,
                "muscle_groups": [
                    {"muscle_group_id": muscle.id, "role": "primary"}
                ]
            }
        )

        assert response.status_code == 422

        assert response.json()["detail"][0]["msg"] == "String should have at least 1 character"


class TestUpdateExercise():
    def test_update_exercise(self, auth_client: TestClient, exercise_factory, equipment_factory, muscle_factory):
        exercise = exercise_factory(
            created_by_user_id=1
        )

        new_equipment = equipment_factory(name="Machine")
        new_muscle = muscle_factory(name="Quads")

        response = auth_client.put(
            f"/exercises/{exercise.id}",
            json={
                "name": "Updated Exercise",
                "equipment_id": new_equipment.id,
                "muscle_groups": [
                    {"muscle_group_id": new_muscle.id, "role": "primary"}
                ]
            }
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["id"] == exercise.id
        assert response_data["name"] == "Updated Exercise"
        assert response_data["equipment"]["id"] == new_equipment.id
        assert len(response_data["muscles"]) == 1
        assert response_data["muscles"][0]["muscle"]["id"] == new_muscle.id
        assert response_data["muscles"][0]["role"] == "primary"


    def test_update_exercise_invalid_id(self, auth_client: TestClient):
        response = auth_client.put(
            "/exercises/20",
            json={
                "name": "Updated Exercise",
                "equipment_id": 1,
                "muscle_groups": [
                    {"muscle_group_id": 1, "role": "primary"}
                ]
            }
        )

        assert response.status_code == 404

        assert response.json()["detail"] == "Exercise with id: 20 not found"

    
    def test_update_exercise_empty_name(self, auth_client: TestClient, exercise_factory):
        exercise = exercise_factory(
            created_by_user_id=1
        )

        response = auth_client.put(
            f"/exercises/{exercise.id}",
            json={
                "name": ""
            }
        )

        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "String should have at least 1 character"

    
    def test_update_exercise_invalid_equipment_id(self, auth_client: TestClient, exercise_factory):
        exercise = exercise_factory(
            created_by_user_id=1
        )

        response = auth_client.put(
            f"/exercises/{exercise.id}",
            json={
                "equipment_id": 20
            }
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Given equipment_id: 20 not found"

    
    def test_update_exercise_invalid_muscle_group_id(self, auth_client: TestClient, exercise_factory):
        exercise = exercise_factory(
            created_by_user_id=1
        )

        response = auth_client.put(
            f"/exercises/{exercise.id}",
            json={
                "muscle_groups": [
                    {"muscle_group_id": 20, "role": "primary"}
                ]
            }
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Given muscle_group_id: 20 not found"


    def test_update_exercise_muscle_group_empty_role(self, auth_client: TestClient, exercise_factory):
        exercise = exercise_factory(
            created_by_user_id=1
        )

        response = auth_client.put(
            f"/exercises/{exercise.id}",
            json={
                "muscle_groups": [
                    {"muscle_group_id": exercise.muscles[0].muscle_group_id, "role": ""}
                ]
            }
        )

        assert response.status_code == 422
        
        assert response.json()["detail"][0]["type"] == "enum"

    def test_update_exercise_other_users_exercise(self, auth_client: TestClient, exercise_factory):
        exercise = exercise_factory(
            created_by_user_id=2
        )

        response = auth_client.put(
            f"/exercises/{exercise.id}",
            json={
                "name": "Updated Exercise"
            }
        )

        assert response.status_code == 404
        assert response.json()["detail"] == f"Exercise with id: {exercise.id} not found"

class TestDeleteExercise():
    def test_delete_exercise(self, auth_client: TestClient, exercise_factory):
        exercise = exercise_factory(
            created_by_user_id=1
        )

        response = auth_client.delete(
            f"/exercises/{exercise.id}"
        )

        assert response.status_code == 204

        response = auth_client.get(
            f"/exercises/{exercise.id}"
        )

        assert response.status_code == 404


    def test_delete_exercise_invalid_id(self, auth_client: TestClient):
        response = auth_client.delete(
            "/exercises/20"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Exercise with id: 20 not found"

    
    def test_delete_exercise_other_users_exercise(self, auth_client: TestClient, exercise_factory):
        exercise = exercise_factory(
            created_by_user_id=2
        )

        response = auth_client.delete(
            f"/exercises/{exercise.id}"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == f"Exercise with id: {exercise.id} not found"