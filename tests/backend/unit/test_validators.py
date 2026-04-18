import pytest
from src.backend.app.validators import (
    validate_title,
    validate_status,
    validate_deadline,
    validate_user_id
)


# ===== TITLE =====
def test_valid_title():
    assert validate_title("Tugas 1") == "Tugas 1"


def test_title_empty():
    with pytest.raises(ValueError):
        validate_title("")


def test_title_whitespace():
    with pytest.raises(ValueError):
        validate_title("   ")


def test_title_not_string():
    with pytest.raises(ValueError):
        validate_title(123)


# ===== STATUS =====
def test_valid_status():
    assert validate_status("pending") == "pending"


def test_invalid_status():
    with pytest.raises(ValueError):
        validate_status("unknown")


# ===== DEADLINE =====
def test_valid_deadline():
    assert validate_deadline("2026-12-31T10:00:00") == "2026-12-31T10:00:00"


def test_invalid_deadline():
    with pytest.raises(ValueError):
        validate_deadline("invalid-date")


def test_none_deadline():
    assert validate_deadline(None) is None


# ===== USER ID =====
def test_valid_user_id():
    assert validate_user_id(1) == 1


def test_user_id_missing():
    with pytest.raises(ValueError):
        validate_user_id(None)


def test_user_id_not_int():
    with pytest.raises(ValueError):
        validate_user_id("abc")