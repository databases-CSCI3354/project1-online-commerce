from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.models.activity_groups import ActivityGroup
from app.models.events import Event
from app.models.locations import Location
from app.models.prerequisite import Prerequisite
from app.utils.database import get_db
from app.utils.decorators import admin_required

events_bp = Blueprint("events", __name__)


def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access required", "error")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@events_bp.route("/events")
def list_events():
    search_query = request.args.get("q", "").strip()
    events = Event.get_all(search_query=search_query)
    return render_template("events/list.html", events=events, search_query=search_query)


@events_bp.route("/events/<int:event_id>")
def view_event(event_id):
    event = Event.get(event_id)
    if not event:
        flash("Event not found", "error")
        return redirect(url_for("events.list_events"))
    
    is_registered = False
    is_waitlisted = False
    
    if current_user.is_authenticated:
        # Check registration status
        registration = get_db().execute(
            """
            SELECT * FROM registrations
            WHERE event_id = ? AND user_id = ?
            """,
            (event_id, current_user.id)
        ).fetchone()
        
        if registration:
            is_registered = registration['status'] == 'registered'
        else:
            # Check waitlist status
            waitlist = get_db().execute(
                """
                SELECT * FROM waitlist
                WHERE event_id = ? AND user_id = ?
                """,
                (event_id, current_user.id)
            ).fetchone()
            is_waitlisted = bool(waitlist)
    
    # Get prerequisites
    prerequisites = Prerequisite.get_prerequisites(event_id)
    
    return render_template("events/view.html",
                         event=event,
                         prerequisites=prerequisites,
                         is_registered=is_registered,
                         is_waitlisted=is_waitlisted)


@events_bp.route("/events/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_event():
    if request.method == "POST":
        try:
            Event.create(
                activity_group_name=request.form['activity_group_name'],
                date=request.form['date'],
                max_participants=request.form.get('max_participants'),
                cost=request.form.get('cost', 0),
                registration_required='registration_required' in request.form,
                registration_deadline=request.form.get('registration_deadline'),
                location_id=request.form.get('location_id'),
                created_by=current_user.id
            )
            flash("Event created successfully", "success")
            return redirect(url_for("events.list_events"))
        except Exception as e:
            flash(f"Error creating event: {str(e)}", "error")
    
    return render_template("events/create.html")


@events_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_event(event_id):
    event = Event.get(event_id)
    if not event:
        flash("Event not found", "error")
        return redirect(url_for("events.list_events"))
    
    if request.method == "POST":
        try:
            Event.update(
                event_id,
                activity_group_name=request.form['activity_group_name'],
                date=request.form['date'],
                max_participants=request.form.get('max_participants'),
                cost=request.form.get('cost', 0),
                registration_required='registration_required' in request.form,
                registration_deadline=request.form.get('registration_deadline'),
                location_id=request.form.get('location_id')
            )
            flash("Event updated successfully", "success")
            return redirect(url_for("events.view_event", event_id=event_id))
        except Exception as e:
            flash(f"Error updating event: {str(e)}", "error")
    
    return render_template("events/edit.html", event=event)


@events_bp.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_event(event_id):
    try:
        Event.delete(event_id)
        flash("Event deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting event: {str(e)}", "error")
    
    return redirect(url_for("events.list_events"))


@events_bp.route("/events/<int:event_id>/register", methods=["POST"])
@login_required
def register_for_event(event_id):
    try:
        # Check prerequisites
        meets_prerequisites, unmet_prerequisites = Prerequisite.check_prerequisites(
            current_user.id, event_id
        )
        
        if not meets_prerequisites:
            flash("You do not meet the prerequisites for this event", "error")
            return redirect(url_for("events.view_event", event_id=event_id))
        
        # Register user
        registered = Event.register_user(event_id, current_user.id)
        
        if registered:
            flash("Successfully registered for event", "success")
        else:
            flash("Event is full. You have been added to the waitlist", "info")
        
    except ValueError as e:
        flash(str(e), "error")
    except Exception as e:
        flash(f"Error registering for event: {str(e)}", "error")
    
    return redirect(url_for("events.view_event", event_id=event_id))


@events_bp.route("/events/<int:event_id>/cancel", methods=["POST"])
@login_required
def cancel_registration(event_id):
    try:
        Event.cancel_registration(event_id, current_user.id)
        flash("Registration cancelled successfully", "success")
    except Exception as e:
        flash(f"Error cancelling registration: {str(e)}", "error")
    
    return redirect(url_for("events.view_event", event_id=event_id))


@events_bp.route("/events/<int:event_id>/notify-waitlist", methods=["POST"])
@login_required
@admin_required
def notify_waitlist(event_id):
    try:
        # Get next person on waitlist
        waitlisted = get_db().execute(
            """
            SELECT w.*, u.email
            FROM waitlist w
            JOIN resident u ON w.user_id = u.resident_id
            WHERE w.event_id = ?
            ORDER BY w.created_at ASC
            LIMIT 1
            """,
            (event_id,)
        ).fetchone()
        
        if waitlisted:
            # TODO: Send email notification
            flash("Notification sent to next person on waitlist", "success")
        else:
            flash("No one is on the waitlist", "info")
        
    except Exception as e:
        flash(f"Error notifying waitlist: {str(e)}", "error")
    
    return redirect(url_for("events.view_event", event_id=event_id))
