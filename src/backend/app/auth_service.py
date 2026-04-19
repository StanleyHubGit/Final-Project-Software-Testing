import jwt
import bcrypt
import os
from datetime import datetime, timedelta
from .models import get_connection

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "super-secret-key-minimal-32-characters!!"
)


class AuthService:

    def register(self, email, password):
        conn = get_connection()
        cursor = conn.cursor()

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")

        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed)
            )
            conn.commit()
        except Exception:
            raise ValueError("User already exists")

        conn.close()

    def login(self, email, password):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if not user:
            raise ValueError("Invalid credentials")

        if not bcrypt.checkpw(password.encode(), user["password"].encode()):
            raise ValueError("Invalid credentials")

        # 🔥 Generate JWT dengan SECRET_KEY dari env
        token = jwt.encode({
            "user_id": user["id"],
            "exp": datetime.utcnow() + timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        return token