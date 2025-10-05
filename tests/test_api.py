import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def create_user(name="Alice", email="alice@example.com", is_active=True):
    res = client.post("/users/", json={"name": name, "email": email, "is_active": is_active})
    assert res.status_code == 201, res.text
    return res.json()


def create_course(title="Python Basics", description="Learn Python", is_open=True):
    res = client.post("/courses/", json={"title": title, "description": description, "is_open": is_open})
    assert res.status_code == 201, res.text
    return res.json()


def enroll(user_id, course_id, enrolled_date="2025-09-16"):
    res = client.post("/enrollments/", json={"user_id": user_id, "course_id": course_id, "enrolled_date": enrolled_date})
    assert res.status_code == 201, res.text
    return res.json()


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] == "EduTrack Lite API"


def test_user_crud_and_deactivate():
    u = create_user()

    res = client.get(f"/users/{u['id']}")
    assert res.status_code == 200

    res = client.put(f"/users/{u['id']}", json={"name": "Alice Smith"})
    assert res.status_code == 200
    assert res.json()["name"] == "Alice Smith"

    res = client.post(f"/users/{u['id']}/deactivate")
    assert res.status_code == 200
    assert res.json()["is_active"] is False

    res = client.delete(f"/users/{u['id']}")
    assert res.status_code == 204


def test_course_crud_and_close_and_list_users():
    c = create_course()
    u1 = create_user(name="Bob", email="bob@example.com")
    u2 = create_user(name="Carol", email="carol@example.com")

    e1 = enroll(u1["id"], c["id"])  # Bob enrolls
    e2 = enroll(u2["id"], c["id"])  # Carol enrolls

    res = client.get(f"/courses/{c['id']}/users")
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 2

    res = client.post(f"/courses/{c['id']}/close")
    assert res.status_code == 200
    assert res.json()["is_open"] is False

    res = client.get(f"/courses/{c['id']}")
    assert res.status_code == 200

    res = client.put(f"/courses/{c['id']}", json={"title": "Python 101"})
    assert res.status_code == 200
    assert res.json()["title"] == "Python 101"

    res = client.delete(f"/courses/{c['id']}")
    assert res.status_code == 204


def test_enrollment_rules_and_views():
    user = create_user(name="Dave", email="dave@example.com")
    course = create_course(title="FastAPI", description="Build APIs")

    e = enroll(user["id"], course["id"])  # first time ok
    assert e["completed"] is False

    # cannot enroll twice
    res = client.post("/enrollments/", json={"user_id": user["id"], "course_id": course["id"], "enrolled_date": "2025-09-16"})
    assert res.status_code == 409

    # mark completion
    res = client.post(f"/enrollments/{e['id']}/complete", json={"completed": True})
    assert res.status_code == 200
    assert res.json()["completed"] is True

    # view enrollments for a user
    res = client.get(f"/enrollments/user/{user['id']}")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 1

    # only active users can enroll
    client.post(f"/users/{user['id']}/deactivate")
    res = client.post("/enrollments/", json={"user_id": user["id"], "course_id": course["id"], "enrolled_date": "2025-09-16"})
    assert res.status_code == 400

    # course must be open
    c2 = create_course(title="Closed Course", description="N/A", is_open=False)
    res = client.post("/enrollments/", json={"user_id": user["id"], "course_id": c2["id"], "enrolled_date": "2025-09-16"})
    assert res.status_code == 400


def test_list_endpoints_empty_and_populated():
    res = client.get("/users/")
    assert res.status_code == 200

    res = client.get("/courses/")
    assert res.status_code == 200

    res = client.get("/enrollments/")
    assert res.status_code == 200
