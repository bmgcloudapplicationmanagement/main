"""SQLite database creation and connection utilities (no external database server)."""

from contextlib import contextmanager
from pathlib import Path
import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS repair_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    email TEXT NOT NULL,
    bicycle_type TEXT NOT NULL,
    service_type TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending'
        CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_repair_requests_created
    ON repair_requests(created_at);
"""


@contextmanager
def database_connection(database_path):
    """Yield a connection, committing on success and rolling back on error."""
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path), timeout=15)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialise_database(database_path):
    """Create schema without discarding or changing existing repair data."""
    with database_connection(database_path) as connection:
        connection.executescript(SCHEMA)
