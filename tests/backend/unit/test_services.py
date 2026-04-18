import pytest
from src.backend.app.services import AssignmentService


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
        "title": "Tugas 1",
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


# ===== GET =====
def test_get_user_assignments(service):
    user_id = 1
    result = service.get_user_assignments(user_id)
    assert isinstance(result, list)


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