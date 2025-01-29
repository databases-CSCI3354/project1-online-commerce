from flask import Blueprint, jsonify, request
from flask_login import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """Handle user login"""
    data = request.get_json()
    # Add your login logic here
    return jsonify({"message": "Login endpoint"})


@auth_bp.route("/profile")
@login_required
def profile():
    """Protected profile route"""
    return render_template("auth/profile.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Handle user logout"""
    # Add your logout logic here
    return jsonify({"message": "Logged out successfully"})
