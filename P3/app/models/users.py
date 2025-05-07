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
    def get(user_id):
        db = User.get_db()
        user = db.execute(
            "SELECT resident_id, username, hashed_password FROM resident WHERE resident_id = ?",
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
