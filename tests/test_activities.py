def test_root_redirects_to_the_activity_page(client):
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_list_activities_returns_activity_data(client, activity_data):
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activity_data


def test_signup_adds_participant(client):
    # Arrange
    email = "new+student@example.com"

    # Act
    response = client.post("/activities/Art%20Club/signup", params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Art Club"}
    assert activities_response.status_code == 200
    assert activities_response.json()["Art Club"]["participants"] == [email]


def test_signup_rejects_existing_participant(client, activity_data):
    # Arrange
    email = "student+test@example.com"
    original_participants = list(activity_data["Chess Club"]["participants"])

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activity_data["Chess Club"]["participants"] == original_participants


def test_signup_rejects_unknown_activity(client):
    # Act
    response = client.post("/activities/Missing/signup", params={"email": "student@example.com"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_requires_email(client):
    # Act
    response = client.post("/activities/Chess%20Club/signup")

    # Assert
    assert response.status_code == 422
