import sqlite3
from datetime import datetime

DATABASE = "database.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        course TEXT,
        deadline TEXT,
        status TEXT DEFAULT 'pending',
        user_id INTEGER,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


class AssignmentRepository:

    def create(self, data):
        conn = get_connection()
        cursor = conn.cursor()

        now = datetime.utcnow().isoformat()

        cursor.execute("""
        INSERT INTO assignments (title, description, course, deadline, status, user_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["title"],
            data.get("description"),
            data.get("course"),
            data.get("deadline"),
            data.get("status", "pending"),
            data["user_id"],
            now,
            now
        ))

        conn.commit()
        assignment_id = cursor.lastrowid
        conn.close()

        return assignment_id

    def get_all_by_user(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM assignments WHERE user_id = ?",
            (user_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    # 🔥 NEW: UPDATE STATUS
    def update_status(self, assignment_id, status):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE assignments SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.utcnow().isoformat(), assignment_id)
        )

        conn.commit()
        conn.close()