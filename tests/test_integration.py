import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_task_success(client):
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Test Task"


def test_add_task_empty(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 400


def test_delete_task_success(client):
    res = client.post("/tasks", json={"title": "Task"})
    task_id = res.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404