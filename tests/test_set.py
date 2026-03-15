from fastapi.testclient import TestClient

from tests.factories import set_factory, workout_factory, exercise_factory, equipment_factory


class TestCreateSet():
    def test_create_set(self, auth_client: TestClient, workout_factory, exercise_factory):
        workout_factory()
        exercise_factory()

        response = auth_client.post(
            "/sets",
            json={
                "workout_id": 1,
                "exercise_id": 1,
                "reps": 8,
                "weight": 135,
                "rest": 30
            }
        )

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["workout_id"] == 1
        assert response_data["exercise_id"] == 1
        assert response_data["reps"] == 8
        assert response_data["weight"] == 135
        assert response_data["rest"] == 30


    def test_create_set_unauth(self, client: TestClient):
        response = client.post(
            "/sets",
            json={
                "workout_id": 1,
                "exercise_id": 1,
                "reps": 8,
                "weight": 135,
                "rest": 30
            }
        )

        assert response.status_code == 401

    
    def test_create_set_defaults(self, auth_client: TestClient, workout_factory, exercise_factory):
        workout_factory()
        exercise_factory()

        response = auth_client.post(
            "/sets",
            json={
                "workout_id": 1,
                "exercise_id": 1,
                "reps": 8
            }
        )

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["workout_id"] == 1
        assert response_data["exercise_id"] == 1
        assert response_data["reps"] == 8
        assert response_data["weight"] == 0
        assert response_data["rest"] == None

    
    def test_create_set_numbering(self, auth_client: TestClient, workout_factory, exercise_factory):
        workout = workout_factory()
        exercise = exercise_factory()

        def create_dummy_set(ex_id):
            return auth_client.post(
                "/sets",
                json={
                    "workout_id": workout.id,
                    "exercise_id": ex_id.id,
                    "reps": 8,
                    "weight": 135,
                    "rest": 30
                }
            )
        
        set_responses = []

        set_responses.append(create_dummy_set(exercise))
        set_responses.append(create_dummy_set(exercise))

        exercise_two = exercise_factory()
        set_responses.append(create_dummy_set(exercise_two))
        
        set_responses.append(create_dummy_set(exercise))

        for i, response in enumerate(set_responses):
            assert response.status_code == 201
            set_responses[i] = response.json()

        assert set_responses[0]["set_number"] == 1
        assert set_responses[1]["set_number"] == 2
        assert set_responses[2]["set_number"] == 1
        assert set_responses[3]["set_number"] == 3


class TestReadSet():
    def test_read_set(self, auth_client: TestClient, set_factory):
        new_set = set_factory()

        response = auth_client.get(
            f"/sets/{new_set.id}"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["workout_id"] == 1
        assert response_data["exercise_id"] == 1
        assert response_data["reps"] == 8
        assert response_data["weight"] == 135
        assert response_data["rest"] == 120

    
    def test_read_set_unauth(self, client: TestClient, set_factory):
        new_set = set_factory()

        response = client.get(
            f"/sets/{new_set.id}"
        )

        assert response.status_code == 401


    def test_read_set_wrong_user(self, auth_client: TestClient, set_factory, workout_factory):
        workout = workout_factory(user_id=12)
        new_set = set_factory(workout_id=workout.id)

        response = auth_client.get(
            f"/sets/{new_set.id}"
        )

        assert response.status_code == 404

    
    def test_read_set_bad_id(self, auth_client: TestClient):
        response = auth_client.get(
            "/sets/210"
        )

        assert response.status_code == 404


class TestUpdateSet():
    def test_update_set(self, auth_client: TestClient, set_factory, exercise_factory):
        new_set = set_factory()
        new_exercise = exercise_factory(name="Shoulder Press")

        response = auth_client.put(
            f"/sets/{new_set.id}",
            json={
                "exercise_id": new_exercise.id,
                "reps": 10,
                "weight": 80,
                "rest": 100
            }
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["workout_id"] == 1
        assert response_data["exercise_id"] == new_exercise.id
        assert response_data["reps"] == 10
        assert response_data["weight"] == 80
        assert response_data["rest"] == 100

    
    def test_update_set_unauth(self, client: TestClient, set_factory):
        new_set = set_factory()

        response = client.put(
            f"/sets/{new_set.id}",
            json={
                "exercise_id": 1,
                "reps": 10,
                "weight": 80,
                "rest": 100
            }
        )

        assert response.status_code == 401

    
    def test_update_set_none(self, auth_client: TestClient, set_factory):
        new_set = set_factory()

        response = auth_client.put(
            f"/sets/{new_set.id}",
            json={}
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["workout_id"] == 1
        assert response_data["exercise_id"] == 1
        assert response_data["reps"] == 8
        assert response_data["weight"] == 135
        assert response_data["rest"] == 120

    
    def test_update_set_wrong_user(self, auth_client: TestClient, set_factory, workout_factory):
        workout = workout_factory(user_id=12)
        new_set = set_factory(workout_id=workout.id)

        response = auth_client.put(
            f"/sets/{new_set.id}",
            json={
                "reps": 400
            }
        )

        assert response.status_code == 404


    def test_update_set_bad_id(self, auth_client: TestClient,):
        response = auth_client.put(
            "/sets/210",
            json={
                "weight": 200
            }
        )

        assert response.status_code == 404


class TestDeleteSet():
    def test_delete_set(self, auth_client: TestClient, set_factory):
        new_set = set_factory()

        response = auth_client.delete(
            f"/sets/{new_set.id}"
        )

        assert response.status_code == 204


    def test_delete_set_unauth(self, client: TestClient, set_factory):
        new_set = set_factory()

        response = client.delete(
            f"/sets/{new_set.id}"
        )

        assert response.status_code == 401


    def test_delete_set_wrong_user(self, auth_client: TestClient, set_factory, workout_factory):
        workout = workout_factory(user_id=12)
        new_set = set_factory(workout_id=workout.id)

        response = auth_client.delete(
            f"/sets/{new_set.id}"
        )

        assert response.status_code == 404


    def test_delete_set_bad_id(self, auth_client: TestClient):
        response = auth_client.delete(
            "/sets/210"
        )

        assert response.status_code == 404