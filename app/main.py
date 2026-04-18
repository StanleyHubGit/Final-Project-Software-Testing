from flask import Flask, request, jsonify
from app.service import create_task, get_all_tasks, delete_task

app = Flask(__name__)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    
    try:
        task = create_task(data.get("title"))
        return jsonify(task), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(get_all_tasks()), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    if delete_task(task_id):
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)