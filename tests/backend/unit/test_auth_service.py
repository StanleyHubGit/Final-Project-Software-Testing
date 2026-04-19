import pytest
from src.backend.app.auth_service import AuthService
from src.backend.app.models import init_db, get_connection


@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    conn = get_connection()
    conn.execute("DELETE FROM users")
    conn.commit()
    conn.close()


def test_register_success():
    service = AuthService()
    service.register("test@mail.com", "123456")

    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", ("test@mail.com",)).fetchone()
    conn.close()

    assert user is not None


def test_register_duplicate():
    service = AuthService()
    service.register("test@mail.com", "123456")

    with pytest.raises(ValueError):
        service.register("test@mail.com", "123456")


def test_login_success():
    service = AuthService()
    service.register("test@mail.com", "123456")

    token = service.login("test@mail.com", "123456")
    assert token is not None


def test_login_user_not_found():
    service = AuthService()

    with pytest.raises(ValueError):
        service.login("notfound@mail.com", "123456")


def test_login_wrong_password():
    service = AuthService()
    service.register("test@mail.com", "123456")

    with pytest.raises(ValueError):
        service.login("test@mail.com", "wrongpass")