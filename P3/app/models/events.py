
from app.utils.database import get_db


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
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO events (activity_group_name, date, location_id, 
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
        event = db.execute("""SELECT * FROM events WHERE id = ?""", (event_id,)).fetchone()

        if event is None:
            return None

        return Event(
            id=event["id"],
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
            """SELECT e.*, l.address, l.city, l.state, l.zip_code,
                      COUNT(p.prerequisite_event_id) as prereq_count
               FROM events e
               LEFT JOIN locations l ON e.location_id = l.id
               LEFT JOIN prerequisites p ON e.id = p.event_id
               GROUP BY e.id
               ORDER BY e.date DESC"""
        ).fetchall()
        return events

    @staticmethod
    def get_by_activity_group(activity_group_name):
        db = get_db()
        events = db.execute(
            """SELECT e.*, l.address, l.city, l.state, l.zip_code
               FROM events e
               LEFT JOIN locations l ON e.location_id = l.id
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
               FROM prerequisites p
               JOIN events e ON p.prerequisite_event_id = e.id
               WHERE p.event_id = ?""",
            (event_id,),
        ).fetchall()
        return prerequisites

    def update(self):
        db = get_db()
        db.execute(
            """UPDATE events
               SET activity_group_name = ?,
                   date = ?,
                   location_id = ?,
                   max_participants = ?,
                   cost = ?,
                   registration_required = ?,
                   registration_deadline = ?
               WHERE id = ?""",
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
        db.execute("DELETE FROM events WHERE id = ?", (self.id,))
        db.commit()
