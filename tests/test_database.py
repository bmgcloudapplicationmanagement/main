"""Test database creation, isolation and persistence across app instances."""

import sqlite3

from dee_cycles_api import create_app
from dee_cycles_api.db import database_connection


def test_database_created_on_first_start(tmp_path):
    path = tmp_path / "nested" / "repairs.db"
    create_app({"TESTING": True, "DATABASE_PATH": str(path)})
    assert path.is_file()
    with sqlite3.connect(path) as connection:
        names = {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )}
    assert "repair_requests" in names


def test_database_persists_between_app_instances(tmp_path, example_request):
    path = tmp_path / "persistent.db"
    first_app = create_app({
        "TESTING": True, "DATABASE_PATH": str(path), "STAFF_API_KEY": "demo"
    })
    created = first_app.test_client().post("/api/repairs", json=example_request)
    repair_id = created.json["id"]

    second_app = create_app({
        "TESTING": True, "DATABASE_PATH": str(path), "STAFF_API_KEY": "demo"
    })
    retrieved = second_app.test_client().get(
        f"/api/repairs/{repair_id}", headers={"X-Staff-Key": "demo"}
    )
    assert retrieved.status_code == 200
    assert retrieved.json["customer_name"] == example_request["customer_name"]


def test_connection_rolls_back_failed_write(tmp_path):
    path = tmp_path / "rollback.db"
    create_app({"TESTING": True, "DATABASE_PATH": str(path)})
    try:
        with database_connection(path) as connection:
            connection.execute(
                """INSERT INTO repair_requests
                   (customer_name,email,bicycle_type,service_type,
                    description,status,created_at)
                   VALUES (?,?,?,?,?,?,?)""",
                ("Test", "test@example.com", "Road", "Basic", "Issue", "Pending", "now"),
            )
            raise RuntimeError("Simulated transaction failure")
    except RuntimeError:
        pass
    with database_connection(path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM repair_requests").fetchone()[0]
    assert count == 0
