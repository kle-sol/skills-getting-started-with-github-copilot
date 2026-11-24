import pytest


def test_unregister_removes_all_matching_entries(client, activity_data):
    # Arrange
    participants = activity_data["Chess Club"]["participants"]
    participants.append("student+test@example.com")
    params = {"email": "student+test@example.com"}

    # Act
    response = client.delete("/activities/Chess%20Club/signup", params=params)
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered student+test@example.com from Chess Club"}
    assert activities_response.status_code == 200
    assert activities_response.json()["Chess Club"]["participants"] == ["other@example.com"]


def test_student_can_sign_up_again_after_unregistering(client):
    # Arrange
    params = {"email": "student+test@example.com"}
    unregister_response = client.delete("/activities/Chess%20Club/signup", params=params)
    assert unregister_response.status_code == 200

    # Act
    response = client.post("/activities/Chess%20Club/signup", params=params)
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert activities_response.status_code == 200
    assert "student+test@example.com" in activities_response.json()["Chess Club"]["participants"]


@pytest.mark.parametrize(
    ("activity", "email", "detail"),
    [
        ("Missing", "student@example.com", "Activity not found"),
        ("Chess%20Club", "missing@example.com", "Student not signed up for this activity"),
    ],
)
def test_unregister_rejects_unknown_activity_or_participant(client, activity_data, activity, email, detail):
    # Arrange
    original_participants = list(activity_data["Chess Club"]["participants"])

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == detail
    assert activity_data["Chess Club"]["participants"] == original_participants


def test_unregister_requires_email(client):
    # Act
    response = client.delete("/activities/Chess%20Club/signup")

    # Assert
    assert response.status_code == 422
