from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
import sys

from app.models.activity_groups import ActivityGroup
from app.models.events import Event
from app.models.locations import Location
from app.utils.database import get_db

events_bp = Blueprint("events", __name__)


@events_bp.route("/events")
def list_events():
    events = Event.get_all()
    event_locations = []
    for row in events:
        event = Event(
            id=row["event_id"],
            activity_group_name=row["activity_group_name"],
            date=row["date"],
            location_id=row["location_id"],
            max_participants=row["max_participants"],
            cost=row["cost"],
            registration_required=row["registration_required"],
            registration_deadline=row["registration_deadline"]
        )
        location = None
        if event.location_id:
            location = Location.get(event.location_id)
        event.prereq_count = row["prereq_count"] if "prereq_count" in row.keys() else 0
        event_locations.append((event, location))
    return render_template("events/list.html", event_locations=event_locations)


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
        location_id_raw = request.form.get("location_id")
        try:
            location_id = int(location_id_raw)
        except (TypeError, ValueError):
            location_id = None
        max_participants = request.form.get("max_participants", type=int)
        cost = request.form.get("cost", type=int)
        registration_required = bool(request.form.get("registration_required"))
        registration_deadline = request.form.get("registration_deadline")

        # Validate the data
        if not activity_group_name or not date or not location_id:
            flash("Activity group name, date, and location are required", "error")
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
    activity_groups = ActivityGroup.get_all()
    locations = Location.get_all()
    return render_template(
        "events/create.html", activity_groups=activity_groups, locations=locations
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
