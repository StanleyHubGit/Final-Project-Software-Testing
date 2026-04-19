from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app)

    # Init DB
    from .models import init_db
    init_db()

    # Config
    app.config["SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    "super-secret-key-minimal-32-characters!!"
    )

    if test_config:
        app.config.update(test_config)

    # Register routes
    from .routes import task_bp
    from .auth_routes import auth_bp

    app.register_blueprint(task_bp, url_prefix="/tasks")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Global error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({"error": str(e)}), 500

    @app.route("/")
    def index():
        return {"message": "Student Assignment Manager API"}

    return app