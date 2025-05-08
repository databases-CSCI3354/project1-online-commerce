import sqlite3

from flask import current_app, g
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()


class User(UserMixin):
    def __init__(self, id, username, resident_id, hashed_password):
        self.id = id
        self.username = username
        self.resident_id = resident_id
        self.hashed_password = hashed_password

    @staticmethod
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(
                current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        return g.db

    @staticmethod
    def validate(username, password):
        db = User.get_db()
        user = db.execute(
            "SELECT resident_id, username, hashed_password FROM resident WHERE username = ?",
            (username,),
        ).fetchone()

        print(f"[DEBUG] DB user: {user}")
        if user is not None:
            print(f"[DEBUG] Hash in DB: {user['hashed_password']}")

        if user is None:
            return None

        if bcrypt.check_password_hash(user["hashed_password"], password):
            print("[DEBUG] Password check: SUCCESS")
            return User(
                user["resident_id"],
                user["username"],
                user["resident_id"],
                user["hashed_password"],
            )
        print("[DEBUG] Password check: FAIL")
        return None

    @staticmethod
    def create(username, resident_id, password):
        """Create a new user with hashed password."""
        if not username or not password:
            raise ValueError("Username and password are required")
        db = User.get_db()
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO resident (username, resident_id, hashed_password)
               VALUES (?, ?, ?)""",
            (username, resident_id, hashed_password),
        )
        db.commit()
        return cursor.lastrowid

    def update_password(self, new_password):
        """Update the user's password."""
        if not new_password:
            raise ValueError("Password cannot be empty")
        db = User.get_db()
        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        db.execute(
            """UPDATE resident
               SET hashed_password = ?
               WHERE resident_id = ?""",
            (hashed_password, self.resident_id),
        )
        db.commit()

    def soft_delete(self):
        """Mark the user as deleted instead of hard deleting."""
        db = User.get_db()
        db.execute(
            """UPDATE resident
               SET is_deleted = 1
               WHERE resident_id = ?""",
            (self.resident_id,),
        )
        db.commit()

    @staticmethod
    def get(user_id):
        db = User.get_db()
        user = db.execute(
            """SELECT resident_id, username, hashed_password
               FROM resident
               WHERE resident_id = ? AND is_deleted = 0""",
            (user_id,),
        ).fetchone()

        if user:
            return User(
                user["resident_id"],
                user["username"],
                user["resident_id"],
                user["hashed_password"],
            )
        return None
