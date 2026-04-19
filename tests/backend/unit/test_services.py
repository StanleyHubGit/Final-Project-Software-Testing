import pytest
from src.backend.app.services import AssignmentService
from src.backend.app.models import init_db, get_connection


@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    conn = get_connection()
    conn.execute("DELETE FROM assignments")
    conn.commit()
    conn.close()


@pytest.fixture
def service():
    return AssignmentService()


# ===== CREATE =====
def test_create_valid_assignment(service):
    data = {
        "title": "Tugas 1",
        "user_id": 1
    }

    result = service.create_assignment(data)
    assert isinstance(result, int)


def test_create_without_title(service):
    with pytest.raises(ValueError):
        service.create_assignment({"user_id": 1})


def test_create_without_user_id(service):
    with pytest.raises(ValueError):
        service.create_assignment({"title": "Test"})


def test_default_status(service):
    data = {
        "title": "Tugas Default",
        "user_id": 1
    }

    assignment_id = service.create_assignment(data)
    assert assignment_id is not None


def test_invalid_deadline(service):
    with pytest.raises(ValueError):
        service.create_assignment({
            "title": "Test",
            "user_id": 1,
            "deadline": "invalid"
        })


def test_invalid_status(service):
    with pytest.raises(ValueError):
        service.create_assignment({
            "title": "Test",
            "user_id": 1,
            "status": "unknown"
        })


# ===== GET =====
def test_get_user_assignments_empty(service):
    result = service.get_user_assignments(1)
    assert result == []


def test_get_user_assignments_with_data(service):
    service.create_assignment({
        "title": "Tugas 1",
        "user_id": 1
    })

    result = service.get_user_assignments(1)
    assert len(result) == 1


def test_get_user_assignments_invalid_user(service):
    with pytest.raises(ValueError):
        service.get_user_assignments(None)


# ===== IS_LATE =====
def test_is_late_true(service):
    assignment = {
        "deadline": "2000-01-01T00:00:00"
    }
    assert service.is_late(assignment) is True


def test_is_late_false(service):
    assignment = {
        "deadline": "2999-01-01T00:00:00"
    }
    assert service.is_late(assignment) is False


def test_is_late_no_deadline(service):
    assignment = {}
    assert service.is_late(assignment) is False


def test_is_late_invalid_format(service):
    with pytest.raises(ValueError):
        service.is_late({"deadline": "invalid"})


# ===== UPDATE STATUS =====
def test_update_status_success(service):
    assignment_id = service.create_assignment({
        "title": "Tugas Update",
        "user_id": 1
    })

    service.update_assignment_status(assignment_id, "submitted")


def test_update_status_invalid(service):
    assignment_id = service.create_assignment({
        "title": "Tugas Update",
        "user_id": 1
    })

    with pytest.raises(ValueError):
        service.update_assignment_status(assignment_id, "invalid_status")