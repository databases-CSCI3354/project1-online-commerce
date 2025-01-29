from flask import Blueprint, jsonify, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Main landing page"""
    return render_template("main/index.html")


@main_bp.route("/api/data")
def get_data():
    """Sample API endpoint"""
    return jsonify({"message": "Success", "data": {"example": "value"}})
