"""REST endpoints: create, list, retrieve and update bicycle repair requests."""

from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request

from .db import database_connection
from .security import staff_access_error
from .validation import REPAIR_STATUSES, validate_repair

api = Blueprint("api", __name__, url_prefix="/api")


def _database_path():
    return current_app.config["DATABASE_PATH"]


@api.get("/health")
def health():
    """Health endpoint for local checks and Performance monitoring."""
    return jsonify({"status": "healthy", "service": "dee-cycles-backend"}), 200


@api.post("/repairs")
def create_repair():
    """Submit one fictional customer's bicycle repair request."""
    payload, errors = validate_repair(request.get_json(silent=True))
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with database_connection(_database_path()) as connection:
        cursor = connection.execute(
            """INSERT INTO repair_requests
               (customer_name, email, bicycle_type, service_type,
                description, status, created_at)
               VALUES (?, ?, ?, ?, ?, 'Pending', ?)""",
            (
                payload["customer_name"],
                payload["email"],
                payload["bicycle_type"],
                payload["service_type"],
                payload["description"],
                created_at,
            ),
        )
        new_id = cursor.lastrowid

    return jsonify({
        "id": new_id,
        "message": "Repair request created",
        "status": "Pending",
        "created_at": created_at,
    }), 201


@api.get("/repairs")
def list_repairs():
    """Staff-only: return all repair requests, most recent ID first."""
    rejection = staff_access_error()
    if rejection is not None:
        return rejection
    with database_connection(_database_path()) as connection:
        rows = connection.execute(
            "SELECT * FROM repair_requests ORDER BY id DESC"
        ).fetchall()
    return jsonify([dict(row) for row in rows]), 200


@api.get("/repairs/<int:repair_id>")
def retrieve_repair(repair_id):
    """Staff-only: return one repair or a 404 response."""
    rejection = staff_access_error()
    if rejection is not None:
        return rejection
    with database_connection(_database_path()) as connection:
        row = connection.execute(
            "SELECT * FROM repair_requests WHERE id = ?", (repair_id,)
        ).fetchone()
    if row is None:
        return jsonify({"error": "Repair request not found"}), 404
    return jsonify(dict(row)), 200


@api.patch("/repairs/<int:repair_id>")
def update_repair(repair_id):
    """Staff-only: change a repair request's status."""
    rejection = staff_access_error()
    if rejection is not None:
        return rejection

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or payload.get("status") not in REPAIR_STATUSES:
        return jsonify({
            "error": "Invalid status",
            "allowed": ["Pending", "In Progress", "Completed"],
        }), 400

    with database_connection(_database_path()) as connection:
        result = connection.execute(
            "UPDATE repair_requests SET status = ? WHERE id = ?",
            (payload["status"], repair_id),
        )
        if result.rowcount == 0:
            return jsonify({"error": "Repair request not found"}), 404

    return jsonify({
        "id": repair_id,
        "message": "Repair status updated",
        "status": payload["status"],
    }), 200
