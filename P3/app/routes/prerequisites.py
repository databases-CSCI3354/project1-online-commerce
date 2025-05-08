from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.models.events import Event
from app.models.prerequisite import Prerequisite

prerequisites_bp = Blueprint("prerequisites", __name__)


@prerequisites_bp.route("/prerequisites/<int:event_id>")
@login_required
def list_prerequisites(event_id):
    prerequisites = Prerequisite.get_prerequisites(event_id)
    event = Event.get(event_id)
    return render_template("prerequisites/list.html", prerequisites=prerequisites, event=event)


@prerequisites_bp.route("/prerequisites/add", methods=["POST"])
@login_required
def add_prerequisite():
    event_id = request.form["event_id"]
    prerequisite_event_id = request.form["prerequisite_event_id"]
    minimum_performance = request.form["minimum_performance"]
    qualification_period = request.form["qualification_period"]
    is_waiver_allowed = bool(request.form.get("is_waiver_allowed"))

    try:
        Prerequisite.add_prerequisite(
            event_id,
            prerequisite_event_id,
            minimum_performance,
            qualification_period,
            is_waiver_allowed,
        )
        flash("Prerequisite added successfully", "success")
    except Exception as e:
        flash(f"Error adding prerequisite: {str(e)}", "error")

    return redirect(url_for("prerequisites.list_prerequisites", event_id=event_id))


@prerequisites_bp.route("/prerequisites/remove", methods=["POST"])
@login_required
def remove_prerequisite():
    event_id = request.form["event_id"]
    prerequisite_event_id = request.form["prerequisite_event_id"]

    try:
        Prerequisite.remove_prerequisite(event_id, prerequisite_event_id)
        flash("Prerequisite removed successfully", "success")
    except Exception as e:
        flash(f"Error removing prerequisite: {str(e)}", "error")

    return redirect(url_for("prerequisites.list_prerequisites", event_id=event_id))
