import uuid

def test_register_endpoint_success(client):
    email = f"{uuid.uuid4()}@mail.com"

    response = client.post("/auth/register", json={
        "email": email,
        "password": "123456"
    })

    assert response.status_code == 201
    assert response.json["message"] == "User created"


def test_register_invalid_json(client):
    response = client.post("/auth/register", json=None)
    assert response.status_code == 400


def test_register_duplicate(client):
    client.post("/auth/register", json={
        "email": "test@mail.com",
        "password": "123456"
    })

    response = client.post("/auth/register", json={
        "email": "test@mail.com",
        "password": "123456"
    })

    assert response.status_code == 400


def test_register_exception(client, monkeypatch):
    from src.backend.app.auth_routes import service

    def mock_register(*args, **kwargs):
        raise Exception("fail")

    monkeypatch.setattr(service, "register", mock_register)

    response = client.post("/auth/register", json={
        "email": "a",
        "password": "b"
    })

    assert response.status_code == 400


def test_login_success(client):
    email = f"{uuid.uuid4()}@mail.com"
    client.post("/auth/register", json={
        "email": "test@mail.com",
        "password": "123456"
    })

    response = client.post("/auth/login", json={
        "email": "test@mail.com",
        "password": "123456"
    })

    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_json(client):
    response = client.post("/auth/login", json=None)
    assert response.status_code == 400


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "test@mail.com",
        "password": "123456"
    })

    response = client.post("/auth/login", json={
        "email": "test@mail.com",
        "password": "wrong"
    })

    assert response.status_code == 401


def test_login_exception(client, monkeypatch):
    from src.backend.app.auth_routes import service

    def mock_login(*args, **kwargs):
        raise Exception("fail")

    monkeypatch.setattr(service, "login", mock_login)

    response = client.post("/auth/login", json={
        "email": "a",
        "password": "b"
    })

    assert response.status_code == 401