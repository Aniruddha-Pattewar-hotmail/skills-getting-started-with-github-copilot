"""Tests for the activities API endpoints."""

import pytest


def test_get_activities(client, reset_activities):
    """Test retrieving all activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify expected activities are present
    assert "Basketball" in activities
    assert "Soccer" in activities
    assert "Art Club" in activities
    assert "Drama Club" in activities
    assert "Debate Team" in activities
    assert "Robotics Club" in activities
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_structure(client, reset_activities):
    """Test that activities have the correct structure."""
    response = client.get("/activities")
    activities = response.json()
    
    activity = activities["Basketball"]
    
    # Verify required fields
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Verify data types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_initial_participants(client, reset_activities):
    """Test initial participants for activities."""
    response = client.get("/activities")
    activities = response.json()
    
    # Verify some activities have initial participants
    assert len(activities["Basketball"]["participants"]) == 1
    assert "alex@mergington.edu" in activities["Basketball"]["participants"]
    
    assert len(activities["Soccer"]["participants"]) == 2
    assert "james@mergington.edu" in activities["Soccer"]["participants"]
    assert "sarah@mergington.edu" in activities["Soccer"]["participants"]
