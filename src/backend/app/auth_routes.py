from flask import Blueprint, request, jsonify
from .auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

service = AuthService()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        service.register(data.get("email"), data.get("password"))
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        token = service.login(data.get("email"), data.get("password"))
        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401