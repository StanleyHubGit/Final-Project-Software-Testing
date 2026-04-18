from .models import AssignmentRepository
from .validators import (
    validate_title,
    validate_status,
    validate_deadline,
    validate_user_id
)
from datetime import datetime


class AssignmentService:

    def __init__(self):
        self.repo = AssignmentRepository()

    def create_assignment(self, data):
        title = validate_title(data.get("title"))
        user_id = validate_user_id(data.get("user_id"))

        status = validate_status(data.get("status", "pending"))
        deadline = validate_deadline(data.get("deadline"))

        cleaned_data = {
            "title": title,
            "user_id": user_id,
            "status": status,
            "deadline": deadline,
            "description": data.get("description"),
            "course": data.get("course")
        }

        return self.repo.create(cleaned_data)

    def get_user_assignments(self, user_id):
        validate_user_id(user_id)
        return self.repo.get_all_by_user(user_id)

    def is_late(self, assignment):
        if not assignment.get("deadline"):
            return False

        try:
            deadline = datetime.fromisoformat(assignment["deadline"])
        except Exception:
            raise ValueError("Invalid deadline format")

        return datetime.utcnow() > deadline

    # 🔥 NEW: UPDATE STATUS
    def update_assignment_status(self, assignment_id, status):
        status = validate_status(status)
        self.repo.update_status(assignment_id, status)