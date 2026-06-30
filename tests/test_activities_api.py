def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Ensemble",
        "Debate Team",
        "Science Club",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities.keys()) == expected_activity_names
    for details in activities.values():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details


def test_signup_for_activity_successfully_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    before_response = client.get("/activities")
    before_count = len(before_response.json()[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    after_response = client.get("/activities")
    participants = after_response.json()[activity_name]["participants"]
    assert email in participants
    assert len(participants) == before_count + 1


def test_signup_for_activity_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_successfully_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    before_response = client.get("/activities")
    before_count = len(before_response.json()[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    after_response = client.get("/activities")
    participants = after_response.json()[activity_name]["participants"]
    assert email not in participants
    assert len(participants) == before_count - 1


def test_unregister_from_activity_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_returns_404_for_not_enrolled_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notenrolled@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
