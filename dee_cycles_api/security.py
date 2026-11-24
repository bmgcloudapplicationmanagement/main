"""Minimal demo-only staff key. Not a replacement for production authentication."""

import hmac
from flask import current_app, jsonify, request


def staff_access_error():
    """Return a Flask response when a staff-only endpoint must be rejected."""
    configured_key = current_app.config.get("STAFF_API_KEY", "")
    if not configured_key:
        return jsonify({"error": "Staff access is not configured"}), 503
    supplied_key = request.headers.get("X-Staff-Key", "")
    if not hmac.compare_digest(supplied_key, configured_key):
        return jsonify({"error": "Valid staff key required"}), 401
    return None
