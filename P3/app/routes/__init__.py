from flask import Flask, Blueprint, render_template
from flask_login import login_required, current_user

from app.routes.auth import auth_bp
from app.routes.events import events_bp
from app.routes.main import main_bp
from app.routes.members import members_bp
from app.routes.prerequisites import prerequisites_bp
from app.routes.reviews import reviews_bp
from app.routes.sessions import sessions_bp

from app.models.events import Event
from app.utils.database import get_db


def init_app(app: Flask):
    """Initialize all blueprints with the app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(prerequisites_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(members_bp)

@main_bp.route('/profile')
@login_required
def profile():
    db = get_db()
    # Registered events
    registered_events = db.execute(
        '''SELECT e.id, e.activity_group_name, e.date
           FROM event e
           JOIN registrations r ON r.event_id = e.id
           WHERE r.user_id = ? AND r.status = 'registered' ''',
        (current_user.id,)
    ).fetchall()
    # Waitlisted events
    waitlisted_events = db.execute(
        '''SELECT e.id, e.activity_group_name, e.date
           FROM event e
           JOIN waitlist w ON w.event_id = e.id
           WHERE w.user_id = ?''',
        (current_user.id,)
    ).fetchall()
    return render_template('profile.html', registered_events=registered_events, waitlisted_events=waitlisted_events)
