from app.utils.database import get_db


class Prerequisite:
    def __init__(self, event_id, prerequisite_event_id, minimum_performance, qualification_period, is_waiver_allowed):
        self.event_id = event_id
        self.prerequisite_event_id = prerequisite_event_id
        self.minimum_performance = minimum_performance
        self.qualification_period = qualification_period
        self.is_waiver_allowed = is_waiver_allowed

    @staticmethod
    def add_prerequisite(event_id, prerequisite_event_id, minimum_performance, qualification_period, is_waiver_allowed):
        if event_id == prerequisite_event_id:
            raise ValueError("An event cannot be its own prerequisite.")
        db = get_db()
        db.execute(
            """INSERT INTO prerequisite (event_id, prerequisite_event_id, minimum_performance, qualification_period, is_waiver_allowed)
               VALUES (?, ?, ?, ?, ?)""",
            (event_id, prerequisite_event_id, minimum_performance, qualification_period, is_waiver_allowed),
        )
        db.commit()

    @staticmethod
    def remove_prerequisite(event_id, prerequisite_event_id):
        db = get_db()
        db.execute(
            """DELETE FROM prerequisite
               WHERE event_id = ? AND prerequisite_event_id = ?""",
            (event_id, prerequisite_event_id),
        )
        db.commit()

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

    @staticmethod
    def get_dependent_events(prerequisite_event_id):
        db = get_db()
        dependent_events = db.execute(
            """SELECT p.*, e.activity_group_name, e.date
               FROM prerequisite p
               JOIN event e ON p.event_id = e.event_id
               WHERE p.prerequisite_event_id = ?""",
            (prerequisite_event_id,),
        ).fetchall()
        return dependent_events
