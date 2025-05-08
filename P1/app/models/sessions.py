from app.utils.database import get_db


class Session:
    def __init__(self, id, activity_group_name, event_id, date, attendance, agenda):
        self.id = id
        self.activity_group_name = activity_group_name
        self.event_id = event_id
        self.date = date
        self.attendance = attendance
        self.agenda = agenda

    @staticmethod
    def create(activity_group_name, event_id, date, attendance, agenda):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO session (activity_group_name, event_id, date, attendance, agenda)
               VALUES (?, ?, ?, ?, ?)""",
            (activity_group_name, event_id, date, attendance, agenda),
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get(session_id):
        db = get_db()
        session = db.execute(
            """SELECT * FROM session WHERE id = ?""", (session_id,)
        ).fetchone()

        if session is None:
            return None

        return Session(
            id=session["id"],
            activity_group_name=session["activity_group_name"],
            event_id=session["event_id"],
            date=session["date"],
            attendance=session["attendance"],
            agenda=session["agenda"],
        )

    @staticmethod
    def get_all():
        db = get_db()
        sessions = db.execute("""SELECT * FROM session ORDER BY date DESC""").fetchall()
        return sessions

    @staticmethod
    def get_by_event(event_id):
        db = get_db()
        sessions = db.execute(
            """SELECT * FROM session WHERE event_id = ? ORDER BY date DESC""",
            (event_id,),
        ).fetchall()
        return sessions

    def update(self):
        db = get_db()
        db.execute(
            """UPDATE session
               SET activity_group_name = ?, event_id = ?, date = ?, attendance = ?, agenda = ?
               WHERE id = ?""",
            (
                self.activity_group_name,
                self.event_id,
                self.date,
                self.attendance,
                self.agenda,
                self.id,
            ),
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM session WHERE id = ?", (self.id,))
        db.commit()
