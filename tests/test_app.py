def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12
    assert data["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_new_participant(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@mergington.edu for Chess Club"
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "newstudent@mergington.edu" in participants


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_student(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_removes_existing_participant(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_for_student_not_signed_up(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "notenrolled@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not signed up for this activity"}