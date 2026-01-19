"""Tests for the signup endpoint."""

import pytest


def test_signup_for_activity_success(client, reset_activities):
    """Test successfully signing up for an activity."""
    response = client.post(
        "/activities/Basketball/signup?email=newemail@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newemail@mergington.edu" in data["message"]
    assert "Basketball" in data["message"]


def test_signup_participant_added(client, reset_activities):
    """Test that participant is actually added to the activity."""
    email = "newemail@mergington.edu"
    
    # Signup
    client.post(f"/activities/Basketball/signup?email={email}")
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Basketball"]["participants"]


def test_signup_duplicate_student(client, reset_activities):
    """Test that signing up the same student twice fails."""
    email = "alex@mergington.edu"
    
    # Try to sign up an already registered student
    response = client.post(f"/activities/Basketball/signup?email={email}")
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signing up for a non-existent activity."""
    response = client.post(
        "/activities/NonexistentActivity/signup?email=newemail@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_multiple_students(client, reset_activities):
    """Test signing up multiple different students."""
    emails = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    for email in emails:
        response = client.post(f"/activities/Art Club/signup?email={email}")
        assert response.status_code == 200
    
    # Verify all were added
    response = client.get("/activities")
    activities = response.json()
    for email in emails:
        assert email in activities["Art Club"]["participants"]


def test_signup_different_activities(client, reset_activities):
    """Test signing the same student up for different activities."""
    email = "newstudent@mergington.edu"
    activities_to_join = ["Basketball", "Soccer", "Chess Club"]
    
    for activity in activities_to_join:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify student is in all activities
    response = client.get("/activities")
    activities = response.json()
    for activity in activities_to_join:
        assert email in activities[activity]["participants"]
