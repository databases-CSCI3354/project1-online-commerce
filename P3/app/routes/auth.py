import sqlite3

from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required, login_user, logout_user

from app.models.users import User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

DATABASE = "./dist/activity.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.validate(username, password)
        if user:
            login_user(user)
            return redirect(url_for("main.index"))

        flash("Invalid username or password")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        resident_id = request.form.get("resident_id")

        if not username or not password or not resident_id:
            flash("All fields are required", "error")
            return render_template("auth/register.html")

        db = get_db()
        try:
            # Check if customer exists
            resident = db.execute("SELECT id FROM residents WHERE id = ?", [resident_id]).fetchone()

            if not resident:
                flash("Invalid Resident ID", "error")
                return render_template("auth/register.html")

            # Create new user
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            db.execute(
                "INSERT INTO users (resident_id, username, hashed_password) VALUES (?, ?, ?)",
                (resident_id, username.lower(), hashed_password),
            )
            db.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:
            flash("Username already exists or Resident ID already registered", "error")
            return render_template("auth/register.html")

    return render_template("auth/register.html")


@auth_bp.route("/profile")
@login_required
def profile():
    db = get_db()
    customer = db.execute(
        "SELECT * FROM residents WHERE id = ?", [current_user.resident_id]
    ).fetchone()

    return render_template("auth/profile.html", customer=customer)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
