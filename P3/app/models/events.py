from app.utils.database import get_db
from app.utils.email import send_waitlist_notification


class Event:
    def __init__(
        self,
        id,
        activity_group_name,
        date,
        location_id,
        max_participants,
        cost,
        registration_required,
        registration_deadline,
    ):
        self.id = id
        self.activity_group_name = activity_group_name
        self.date = date
        self.location_id = location_id
        self.max_participants = max_participants
        self.cost = cost
        self.registration_required = registration_required
        self.registration_deadline = registration_deadline

    @property
    def event_id(self):
        return self.id

    @staticmethod
    def create(
        activity_group_name,
        date,
        location_id,
        max_participants,
        cost,
        registration_required,
        registration_deadline,
    ):
        if max_participants < 0 or cost < 0:
            raise ValueError("Max participants and cost must be non-negative")
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO event (activity_group_name, date, location_id, 
                                max_participants, cost, registration_required, 
                                registration_deadline)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                activity_group_name,
                date,
                location_id,
                max_participants,
                cost,
                registration_required,
                registration_deadline,
            ),
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get(event_id):
        db = get_db()
        event = db.execute("""SELECT * FROM event WHERE event_id = ?""", (event_id,)).fetchone()

        if event is None:
            return None

        return Event(
            id=event["event_id"],
            activity_group_name=event["activity_group_name"],
            date=event["date"],
            location_id=event["location_id"],
            max_participants=event["max_participants"],
            cost=event["cost"],
            registration_required=event["registration_required"],
            registration_deadline=event["registration_deadline"],
        )

    @staticmethod
    def get_all():
        db = get_db()
        events = db.execute(
            """SELECT e.*, l.address, l.city, l.state, l.zip_code
               FROM event e
               LEFT JOIN location l ON e.location_id = l.location_id
               ORDER BY e.date ASC"""
        ).fetchall()
        return events

    @staticmethod
    def get_by_activity_group(activity_group_name):
        db = get_db()
        events = db.execute(
            """SELECT e.*, l.address, l.city, l.state, l.zip_code
               FROM event e
               LEFT JOIN location l ON e.location_id = l.location_id
               WHERE e.activity_group_name = ?
               ORDER BY e.date DESC""",
            (activity_group_name,),
        ).fetchall()
        return events

    @staticmethod
    def get_prerequisites(event_id):
        db = get_db()
        prerequisites = db.execute(
            """SELECT p.*, e.activity_group_name, e.date
               FROM prerequisite p
               JOIN event e ON p.prerequisite_event_id = e.event_id
               WHERE p.event_id = ?""",
            (event_id,),
        ).fetchall()
        return prerequisites

    def update(self):
        db = get_db()
        db.execute(
            """UPDATE event
               SET activity_group_name = ?,
                   date = ?,
                   location_id = ?,
                   max_participants = ?,
                   cost = ?,
                   registration_required = ?,
                   registration_deadline = ?
               WHERE event_id = ?""",
            (
                self.activity_group_name,
                self.date,
                self.location_id,
                self.max_participants,
                self.cost,
                self.registration_required,
                self.registration_deadline,
                self.id,
            ),
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM event WHERE event_id = ?", (self.id,))
        db.commit()
    
    @staticmethod
    def event_registration(event_id, user_id):
        db = get_db()
        event = db.execute(
            """SELECT max_participants, 
                      (SELECT count(*) FROM registrations WHERE event_id = ?) AS current_participants
               FROM events WHERE id = ?""",
            (event_id, event_id)
        ).fetchone()

        if not event:
            return {"success": False, "message": "Event not found"}

        if event["current_participants"] < event["max_participants"]:
            db.execute(
                """INSERT INTO registrations (event_id, user_id)
                   VALUES (?, ?)""",
                (event_id, user_id),
            )
            db.commit()
            return {"success": True, "message": "Successfully registered for the event"}

        # Check if the user is already on the waitlist
        if Event.get_waitlist(user_id, event_id):
            return {"success": False, "message": "User is already on the waitlist"}

        # Add the user to the waitlist
        db.execute(
            """INSERT INTO waitlist (event_id, user_id)
               VALUES (?, ?)""",
            (event_id, user_id),
        )
        db.commit()
        return {"success": True, "message": "Event is full. Added to the waitlist"}

    def soft_delete(self):
        """Mark the event as deleted instead of hard deleting."""
        db = get_db()
        db.execute(
            """UPDATE events
               SET is_deleted = 1
               WHERE id = ?""",
            (self.id,),
        )
        db.commit()

    @staticmethod
    def notify_waitlist(event_id):
        db = get_db()
        waitlist_user = db.execute(
            """SELECT w.id, w.user_id, r.email
               FROM waitlist w
               JOIN resident r ON w.user_id = r.resident_id
               WHERE w.event_id = ? AND w.status = 'waiting'
               ORDER BY w.added_at ASC
               LIMIT 1""",
            (event_id,),
        ).fetchone()

        if not waitlist_user:
            return {"success": False, "message": "No users on the waitlist"}

        # Simulate sending a notification
        print(f"Notifying user {waitlist_user['email']} about an open spot in event {event_id}")

        # Update waitlist status to 'notified'
        db.execute(
            """UPDATE waitlist
               SET status = 'notified'
               WHERE id = ?""",
            (waitlist_user["id"],),
        )
        db.commit()
        return {"success": True, "message": "User notified", "email": waitlist_user["email"]}

    @staticmethod
    def confirm_waitlist(event_id, user_id):
        db = get_db()
        waitlist_entry = db.execute(
            """SELECT * FROM waitlist
               WHERE event_id = ? AND user_id = ? AND status = 'notified'""",
            (event_id, user_id),
        ).fetchone()

        if not waitlist_entry:
            return {"success": False, "message": "No notification found for this user"}

        # Register the user
        db.execute(
            """INSERT INTO registrations (event_id, user_id)
               VALUES (?, ?)""",
            (event_id, user_id),
        )
        db.commit()

        # Remove the user from the waitlist
        db.execute(
            """DELETE FROM waitlist
               WHERE id = ?""",
            (waitlist_entry["id"],),
        )
        db.commit()
        return {"success": True, "message": "Waitlist spot confirmed and registered"}

    @staticmethod
    def event_notification():
        db = get_db()
        events = db.execute(
            """SELECT e.id, e.activity_group_name, e.date, u.email
            FROM event e
            JOIN registrations r ON r.event_id = e.id 
            JOIN users u ON r.user_id = u.id
            WHERE e.date BETWEEN datetime('now') AND datetime('now', '+1 day')"""
        ).fetchall()

        for event in events:
            print(f"Sending notification to {event['email']} for event {event['activity_group_name']}")


    @staticmethod
    def search_events(search_term, date, location):
        db = get_db()
        query = """SELECT e.id, e.activity_group_name, e.date, e.location_id
                FROM event e
                LEFT JOIN locations l on e.location_id = l.id
                WHERE 1=1"""
        params = []
        if search_term:
            query += " AND e.activity_group_name LIKE ?"
            params.append(f"%{search_term}%")
        if date:
            query += " AND e.date = ?"
            params.append(date)
        if location:
            query += " AND (l.address LIKE ? OR l.city LIKE ? OR l.state LIKE ? OR l.zip_code LIKE ?)"
            params.extend([f"%{location}%", f"%{location}%", f"%{location}%", f"%{location}%"])
        query += " ORDER BY e.date DESC"
        return db.execute(query, params).fetchall()
   
    @staticmethod
    def get_waitlist(user_id, event_id):
        db = get_db()
        waitlist = db.execute(
            """SELECT w.id, w.event_id, w.user_id
            FROM waitlist w
            JOIN events e ON e.id = w.event_id
            JOIN users u ON u.id = w.user_id
            WHERE w.event_id = ? AND w.user_id = ?""",
            (event_id, user_id)
        ).fetchall()
        return waitlist
