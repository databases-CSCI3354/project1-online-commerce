from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.models.activity_groups import ActivityGroup
from app.models.events import Event
from app.models.locations import Location
from app.utils.database import get_db

events_bp = Blueprint("events", __name__)


@events_bp.route("/events")
def list_events():
    events = Event.get_all()
    return render_template("events/list.html", events=events)


@events_bp.route("/events/<int:event_id>")
def view_event(event_id):
    event = Event.get(event_id)
    if event is None:
        flash("Event not found", "error")
        return redirect(url_for("events.list_events"))

    location = Location.get(event.location_id) if event.location_id else None
    prerequisites = Event.get_prerequisites(event_id)

    return render_template(
        "events/view.html", event=event, location=location, prerequisites=prerequisites
    )


@events_bp.route("/events/create", methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "POST":
        activity_group_name = request.form["activity_group_name"]
        date = request.form["date"]
        location_id = request.form.get("location_id")
        max_participants = request.form.get("max_participants", type=int)
        cost = request.form.get("cost", type=int)
        registration_required = bool(request.form.get("registration_required"))
        registration_deadline = request.form.get("registration_deadline")

        # Validate the data
        if not activity_group_name or not date:
            flash("Activity group name and date are required", "error")
            return redirect(url_for("events.create_event"))

        try:
            event_id = Event.create(
                activity_group_name=activity_group_name,
                date=date,
                location_id=location_id,
                max_participants=max_participants,
                cost=cost,
                registration_required=registration_required,
                registration_deadline=registration_deadline,
            )
            flash("Event created successfully", "success")
            return redirect(url_for("events.view_event", event_id=event_id))
        except Exception as e:
            flash(f"Error creating event: {str(e)}", "error")
            return redirect(url_for("events.create_event"))

    # GET request - show the create form
    locations = Location.get_all()
    activity_groups = ActivityGroup.get_all()
    return render_template(
        "events/create.html", locations=locations, activity_groups=activity_groups
    )


@events_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    event = Event.get(event_id)
    if event is None:
        flash("Event not found", "error")
        return redirect(url_for("events.list_events"))

    if request.method == "POST":
        event.activity_group_name = request.form["activity_group_name"]
        event.date = request.form["date"]
        event.location_id = request.form.get("location_id")
        event.max_participants = request.form.get("max_participants", type=int)
        event.cost = request.form.get("cost", type=int)
        event.registration_required = bool(request.form.get("registration_required"))
        event.registration_deadline = request.form.get("registration_deadline")

        try:
            event.update()
            flash("Event updated successfully", "success")
            return redirect(url_for("events.view_event", event_id=event_id))
        except Exception as e:
            flash(f"Error updating event: {str(e)}", "error")

    locations = Location.get_all()
    activity_groups = ActivityGroup.get_all()
    return render_template(
        "events/edit.html", event=event, locations=locations, activity_groups=activity_groups
    )


@events_bp.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):
    event = Event.get(event_id)
    if event is None:
        flash("Event not found", "error")
    else:
        try:
            event.delete()
            flash("Event deleted successfully", "success")
        except Exception as e:
            flash(f"Error deleting event: {str(e)}", "error")

    return redirect(url_for("events.list_events"))


@events_bp.route("/events/<int:event_id>/prerequisites", methods=["GET", "POST"])
@login_required
def manage_prerequisites(event_id):
    event = Event.get(event_id)
    if event is None:
        flash("Event not found", "error")
        return redirect(url_for("events.list_events"))

    if request.method == "POST":
        prerequisite_event_id = request.form.get("prerequisite_event_id", type=int)
        minimum_performance = request.form.get("minimum_performance", type=int)
        qualification_period = request.form.get("qualification_period", type=int)
        is_waiver_allowed = bool(request.form.get("is_waiver_allowed"))

        db = get_db()
        try:
            db.execute(
                """INSERT INTO prerequisite 
                   (event_id, prerequisite_event_id, minimum_performance,
                    qualification_period, is_waiver_allowed)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    event_id,
                    prerequisite_event_id,
                    minimum_performance,
                    qualification_period,
                    is_waiver_allowed,
                ),
            )
            db.commit()
            flash("Prerequisite added successfully", "success")
        except Exception as e:
            flash(f"Error adding prerequisite: {str(e)}", "error")

    prerequisites = Event.get_prerequisites(event_id)
    other_events = Event.get_by_activity_group(event.activity_group_name)

    return render_template(
        "events/prerequisites.html",
        event=event,
        prerequisites=prerequisites,
        other_events=other_events,
    )


@events_bp.route("/events/<int:event_id>/notify_waitlist", methods=["POST"])
@login_required
def notify_waitlist(event_id):
    result = Event.notify_waitlist(event_id)
    flash(result["message"], "success" if result["success"] else "error")
    return redirect(url_for("events.view_event", event_id=event_id))


@events_bp.route("/events/<int:event_id>/confirm_waitlist", methods=["POST"])
@login_required
def confirm_waitlist(event_id):
    user_id = request.form.get("user_id", type=int)
    result = Event.confirm_waitlist(event_id, user_id)
    flash(result["message"], "success" if result["success"] else "error")
    return redirect(url_for("events.view_event", event_id=event_id))
