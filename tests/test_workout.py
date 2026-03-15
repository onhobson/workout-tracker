from datetime import datetime

from fastapi.testclient import TestClient

from app.core.limits import WORKOUT_NAME_MAX_LENGTH, NOTES_MAX_LENGTH
from tests.factories import workout_factory

class TestCreateWorkout():
    def test_create_workout(self, auth_client: TestClient):
        response = auth_client.post(
            "/workouts",
            json={
                "name": "Workout Name",
                "notes": "Workout notes"
            }
        )

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["name"] == "Workout Name"
        assert response_data["notes"] == "Workout notes"
        assert response_data["user_id"] == 1
        assert response_data["created_at"] is not None

    
    def test_create_workout_unauth(self, client: TestClient):
        response = client.post(
            "/workouts",
            json={
                "name": "Workout Name",
                "notes": "Workout notes"
            }
        )

        assert response.status_code == 401

    
    def test_create_workout_default_name(self, auth_client: TestClient):
        def workout_no_name():
            return auth_client.post(
                "/workouts",
                json={
                    "notes": "Workout notes"
                }
            )
        
        response = workout_no_name()

        assert response.status_code == 201

        response_data = response.json()
        default_name = f"Workout on {datetime.now().strftime('%b %d, %Y')}"

        assert response_data["name"] == default_name
        assert response_data["notes"] == "Workout notes"

        response = workout_no_name()

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["name"] == default_name + " (2)"
        assert response_data["notes"] == "Workout notes"


    def test_create_workout_no_notes(self, auth_client: TestClient):
        response = auth_client.post(
            "/workouts",
            json={
                "name": "Workout"
            }
        )

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["name"] == "Workout"
        assert response_data["notes"] == None

    
    def test_create_workout_name_max_length(self, auth_client: TestClient):
        a_very_long_name = "a" * (WORKOUT_NAME_MAX_LENGTH + 12)
        response = auth_client.post(
            "/workouts",
            json={
                "name": a_very_long_name,
                "notes": "notes"
            }
        )

        assert response.status_code == 422


    def test_create_workout_notes_max_length(self, auth_client: TestClient):
        very_long_notes = "a" * (NOTES_MAX_LENGTH + 12)
        response = auth_client.post(
            "/workouts",
            json={
                "name": "Workout",
                "notes": very_long_notes
            }
        )

        assert response.status_code == 422
    
    
class TestReadWorkout():
    def test_get_workout_by_id(self, auth_client: TestClient, workout_factory):
         workout = workout_factory()

         response = auth_client.get(
             f"/workouts/{workout.id}"
         )

         assert response.status_code == 200

         response_data = response.json()

         assert response_data["name"] == "Test Workout"
         assert response_data["notes"] == "Test notes"
         assert response_data["user_id"] == 1

    
    def test_get_workout_by_id_wrong_user(self, auth_client: TestClient, workout_factory):
        workout = workout_factory(user_id=12)

        response = auth_client.get(
            f"/workouts/{workout.id}"
        )

        assert response.status_code == 404

    
    def test_get_user_workouts(self, auth_client: TestClient, workout_factory):
        workout_factory()
        workout_factory(name="Second", notes="More")

        response = auth_client.get(
            "/workouts"
        )

        assert response.status_code == 200

        response_data = response.json()

        assert isinstance(response_data, list)
        assert len(response_data) == 2

        assert response_data[0]["name"] == "Test Workout"
        assert response_data[0]["notes"] == "Test notes"
        assert response_data[0]["user_id"] == 1

        assert response_data[1]["name"] == "Second"
        assert response_data[1]["notes"] == "More"
        assert response_data[1]["user_id"] == 1

    
    def test_get_workout_bad_id(self, auth_client: TestClient):
        response = auth_client.get(
            "/workouts/202"
        )

        assert response.status_code == 404

    
class TestUpdateWorkout():
    def test_update_workout(self, auth_client: TestClient, workout_factory):
        workout = workout_factory()

        response = auth_client.put(
            f"/workouts/{workout.id}",
            json={
                "name": "New name",
                "notes": "New notes"
            }
        )

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["name"] == "New name"
        assert response_data["notes"] == "New notes"

    
    def test_update_workout_unauth(self, client: TestClient, workout_factory):
        workout = workout_factory()

        response = client.put(
            f"/workouts/{workout.id}",
            json={
                "name": "New name",
                "notes": "New notes"
            }
        )

        assert response.status_code == 401
        
        assert workout.name == "Test Workout"
        assert workout.notes == "Test notes"

    
    def test_update_workout_wrong_user(self, auth_client: TestClient, workout_factory):
        workout = workout_factory(user_id=12)

        response = auth_client.put(
            f"/workouts/{workout.id}",
            json={
                "name": "New name",
                "notes": "New notes"
            }
        )

        assert response.status_code == 404
        
        assert workout.name == "Test Workout"
        assert workout.notes == "Test notes"
        

    def test_update_workout_bad_id(self, auth_client: TestClient):
        response = auth_client.put(
            "/workouts/202",
            json={
                "name": "Workout"
            }
        )

        assert response.status_code == 404


class TestDeleteWorkout():
    def test_delete_workout(self, auth_client: TestClient, workout_factory):
        workout = workout_factory()

        response = auth_client.delete(
            f"/workouts/{workout.id}"
        )

        assert response.status_code == 204

    
    def test_delete_workout_unauth(self, client: TestClient, workout_factory):
        workout = workout_factory()

        response = client.delete(
            f"/workouts/{workout.id}"
        )

        assert response.status_code == 401


    def test_delete_workout_wrong_user(self, auth_client: TestClient, workout_factory):
        workout = workout_factory(user_id=12)

        response = auth_client.delete(
            f"/workout/{workout.id}"
        )

        assert response.status_code == 404

        
    def test_delete_workout_bad_id(self, auth_client: TestClient):
        response = auth_client.delete(
            "/workouts/202"
        )

        assert response.status_code == 404
