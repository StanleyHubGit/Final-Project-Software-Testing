import pytest


def test_create_task(client):
    response = client.post("/tasks/", json={
        "title": "Tugas Integrasi",
        "user_id": 1
    })

    assert response.status_code == 201
    assert "id" in response.json


def test_create_task_invalid(client):
    response = client.post("/tasks/", json={
        "user_id": 1
    })

    assert response.status_code == 400


def test_get_tasks_empty(client):
    response = client.get("/tasks/?user_id=999")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_tasks_after_create(client):
    client.post("/tasks/", json={
        "title": "Tugas 1",
        "user_id": 1
    })

    response = client.get("/tasks/?user_id=1")

    assert response.status_code == 200
    assert len(response.json) >= 1


def test_get_tasks_invalid_user(client):
    response = client.get("/tasks/?user_id=abc")
    assert response.status_code == 400


# 🔥 TAMBAHAN (WAJIB UNTUK 100%)
def test_update_status_endpoint(client):
    res = client.post("/tasks/", json={
        "title": "Test",
        "user_id": 1
    })

    task_id = res.json["id"]

    response = client.put(f"/tasks/{task_id}/status", json={
        "status": "submitted"
    })

    assert response.status_code == 200


def test_update_status_invalid(client):
    res = client.post("/tasks/", json={
        "title": "Test",
        "user_id": 1
    })

    task_id = res.json["id"]

    response = client.put(f"/tasks/{task_id}/status", json={
        "status": "invalid_status"
    })

    assert response.status_code == 400