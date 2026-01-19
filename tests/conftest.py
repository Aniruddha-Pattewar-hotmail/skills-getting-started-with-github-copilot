"""Pytest configuration and fixtures for the FastAPI app tests."""

import pytest
import sys
from pathlib import Path

# Add src directory to path to import the app module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    from app import activities
    
    # Store original state
    original_activities = {
        "Basketball": {
            "description": "Team basketball training and games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer": {
            "description": "Soccer practice and friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["james@mergington.edu", "sarah@mergington.edu"]
        },
        "Art Club": {
            "description": "Drawing, painting, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performance and script writing",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 14,
            "participants": ["noah@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots for competitions",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["grace@mergington.edu", "tyler@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup - reset after test
    activities.clear()
    activities.update(original_activities)
