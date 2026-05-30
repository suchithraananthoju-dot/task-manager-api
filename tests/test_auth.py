from fastapi.testclient import TestClient
from main import app
import uuid


client = TestClient(app)


def test_signup():

    unique_username = f"user_{uuid.uuid4().hex[:6]}"

    response = client.post(
        "/signup",
        json={
            "username": unique_username,
            "password": "1234"
        }
    )

    assert response.status_code == 200

def test_login():

    response = client.post(
        "/login",
        json={
            "username": "suchi",
            "password": "1234"
        }
    )

    assert response.status_code == 200

def test_invalid_login():

    response = client.post(
        "/login",
        json={
            "username": "suchi",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

def test_get_tasks_without_token():

    response = client.get("/tasks")

    assert response.status_code == 401