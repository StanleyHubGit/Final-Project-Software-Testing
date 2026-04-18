from flask import Blueprint, request, jsonify
from .services import AssignmentService

task_bp = Blueprint("tasks", __name__)
service = AssignmentService()


@task_bp.route("/", methods=["POST"])
def create_task():
    data = request.json

    try:
        assignment_id = service.create_assignment(data)
        return jsonify({"id": assignment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@task_bp.route("/", methods=["GET"])
def get_tasks():
    user_id = request.args.get("user_id", type=int)

    try:
        tasks = service.get_user_assignments(user_id)
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 🔥 NEW: UPDATE STATUS
@task_bp.route("/<int:id>/status", methods=["PUT"])
def update_status(id):
    data = request.json

    try:
        service.update_assignment_status(id, data.get("status"))
        return jsonify({"message": "Updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400