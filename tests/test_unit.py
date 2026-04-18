import pytest
from app.service import create_task, get_all_tasks, delete_task
from app.model import tasks

def setup_function():
    tasks.clear()


def test_create_task_success():
    task = create_task("Test Task")
    assert task["title"] == "Test Task"
    assert task["done"] == False


def test_create_task_empty():
    with pytest.raises(ValueError):
        create_task("")


def test_create_task_none():
    with pytest.raises(ValueError):
        create_task(None)


def test_get_all_tasks_empty():
    assert get_all_tasks() == []


def test_get_all_tasks_with_data():
    create_task("Task 1")
    assert len(get_all_tasks()) == 1


def test_delete_task_success():
    task = create_task("Task 1")
    result = delete_task(task["id"])
    assert result == True


def test_delete_task_not_found():
    result = delete_task(999)
    assert result == False


def test_multiple_tasks():
    create_task("Task 1")
    create_task("Task 2")
    assert len(get_all_tasks()) == 2


def test_task_ids_unique():
    t1 = create_task("Task 1")
    t2 = create_task("Task 2")
    assert t1["id"] != t2["id"]


def test_delete_one_of_many():
    t1 = create_task("Task 1")
    t2 = create_task("Task 2")
    delete_task(t1["id"])
    assert len(get_all_tasks()) == 1


def test_create_task_strip_spaces():
    task = create_task("  Hello  ")
    assert task["title"] == "  Hello  "


def test_delete_all_tasks():
    t1 = create_task("Task 1")
    t2 = create_task("Task 2")
    delete_task(t1["id"])
    delete_task(t2["id"])
    assert get_all_tasks() == []


def test_create_many_tasks():
    for i in range(5):
        create_task(f"Task {i}")
    assert len(get_all_tasks()) == 5


def test_delete_invalid_type():
    result = delete_task("abc")
    assert result == False


def test_task_structure():
    task = create_task("Test")
    assert "id" in task
    assert "title" in task
    assert "done" in task