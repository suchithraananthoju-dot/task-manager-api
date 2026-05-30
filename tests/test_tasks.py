from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


# Create unique user
username = f"user_{uuid.uuid4().hex[:6]}"
password = "1234"


# Signup User
client.post(
    "/signup",
    json={
        "username": username,
        "password": password
    }
)


# Login User
login_response = client.post(
    "/login",
    json={
        "username": username,
        "password": password
    }
)

token = login_response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}


# Test Create Task
def test_create_task():

    response = client.post(
        "/tasks",
        json={
            "title": "Learn Pytest",
            "description": "Testing FastAPI project"
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn Pytest"


# Test Get Tasks
def test_get_tasks():

    response = client.get(
        "/tasks",
        headers=headers
    )

    assert response.status_code == 200
    assert type(response.json()) == list


# Test Update Task
def test_update_task():

    # First create task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Old Task",
            "description": "Old Description"
        },
        headers=headers
    )

    task_id = create_response.json()["id"]

    # Update task
    update_response = client.put(
    f"/tasks/{task_id}",
    json={
        "title": "Updated Task",
        "description": "Updated Description",
        "status": "completed"
    },
    headers=headers
)

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Task"


# Test Delete Task
def test_delete_task():

    # First create task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete Task",
            "description": "To be deleted"
        },
        headers=headers
    )

    task_id = create_response.json()["id"]

    # Delete task
    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers=headers
    )

    assert delete_response.status_code == 200


def test_delete_invalid_task():

    response = client.delete(
        "/tasks/99999",
        headers=headers
    )

    assert response.status_code == 404

def test_update_invalid_task():

    response = client.put(
        "/tasks/99999",
        json={
            "title": "Test",
            "description": "Test Desc",
            "status": "completed"
        },
        headers=headers
    )

    assert response.status_code == 404