import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# GET /activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

# POST /activities/{activity_name}/signup
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "another@mergington.edu")
])
def test_signup_for_activity(activity, email):
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400

# POST /activities/{activity_name}/unregister
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "michael@mergington.edu"),
    ("Programming Class", "emma@mergington.edu")
])
def test_unregister_from_activity(activity, email):
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Unregister again should fail
    response2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 400

# POST /activities/{activity_name}/signup for non-existent activity
def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404

# POST /activities/{activity_name}/unregister for non-existent activity
def test_unregister_nonexistent_activity():
    response = client.post("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
