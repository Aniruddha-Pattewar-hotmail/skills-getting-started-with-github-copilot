"""Tests for the unregister endpoint."""

import pytest


def test_unregister_success(client, reset_activities):
    """Test successfully unregistering a student from an activity."""
    email = "alex@mergington.edu"
    
    response = client.post(
        f"/activities/Basketball/unregister?email={email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Basketball" in data["message"]


def test_unregister_participant_removed(client, reset_activities):
    """Test that participant is actually removed from the activity."""
    email = "alex@mergington.edu"
    
    # Unregister
    client.post(f"/activities/Basketball/unregister?email={email}")
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Basketball"]["participants"]


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregistering from a non-existent activity."""
    response = client.post(
        "/activities/NonexistentActivity/unregister?email=alex@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_not_registered_student(client, reset_activities):
    """Test unregistering a student who isn't registered."""
    response = client.post(
        "/activities/Basketball/unregister?email=notregistered@mergington.edu"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_then_signup_again(client, reset_activities):
    """Test unregistering and then signing up again."""
    email = "alex@mergington.edu"
    
    # Unregister
    response = client.post(f"/activities/Basketball/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify removed
    response = client.get("/activities")
    assert email not in response.json()["Basketball"]["participants"]
    
    # Sign up again
    response = client.post(f"/activities/Basketball/signup?email={email}")
    assert response.status_code == 200
    
    # Verify added again
    response = client.get("/activities")
    assert email in response.json()["Basketball"]["participants"]


def test_unregister_multiple_students(client, reset_activities):
    """Test unregistering multiple students from an activity."""
    # Soccer has ["james@mergington.edu", "sarah@mergington.edu"]
    emails = ["james@mergington.edu", "sarah@mergington.edu"]
    
    for email in emails:
        response = client.post(f"/activities/Soccer/unregister?email={email}")
        assert response.status_code == 200
    
    # Verify all were removed
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Soccer"]["participants"]) == 0
