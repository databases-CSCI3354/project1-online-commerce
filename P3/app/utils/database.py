import sqlite3

from flask import current_app, g

from app.utils.logger import setup_logger

log = setup_logger(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        # Enable foreign key constraints
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def check_db_health():
    """Check if the database is accessible and has the correct schema."""
    try:
        db = get_db()
        # Check if essential tables exist
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        required_tables = {"resident", "activity_group", "event", "review"}
        existing_tables = {table["name"] for table in tables}

        missing_tables = required_tables - existing_tables
        if missing_tables:
            log.error(f"Missing required tables: {missing_tables}")
            return False

        # Check if test user exists
        test_user = db.execute(
            "SELECT resident_id FROM resident WHERE username = 'testuser'"
        ).fetchone()
        if not test_user:
            log.warning("Test user not found in database")
            return False

        return True
    except Exception as e:
        log.error(f"Database health check failed: {str(e)}")
        return False
