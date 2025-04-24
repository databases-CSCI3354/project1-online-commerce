from flask import Blueprint, render_template

from app.services.activity_groups import ActivityGroupsService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    """Main landing page"""
    activity_groups_service = ActivityGroupsService()
    all_activity_groups = activity_groups_service.get_all_activity_groups()
    return render_template("main/index.html", all_activity_groups=all_activity_groups)
