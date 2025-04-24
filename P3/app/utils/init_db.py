import sqlite3

from app.utils.logger import setup_logger

log = setup_logger(__name__)


def init_db(app):
    """Initialize the database with required tables."""
    with app.app_context():
        db = sqlite3.connect(
            app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.execute("PRAGMA foreign_keys = ON")
        with open("app/utils/schema.sql", "r") as f:
            db.executescript(f.read())

        db.commit()
