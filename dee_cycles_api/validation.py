"""Input validation for fictional bicycle repair requests."""

import re

SERVICE_TYPES = frozenset({"Basic", "Standard", "Deluxe", "Other"})
REPAIR_STATUSES = frozenset({"Pending", "In Progress", "Completed"})

FIELDS = {
    "customer_name": 100,
    "email": 254,
    "bicycle_type": 80,
    "service_type": 30,
    "description": 2000,
}

# Appropriate for basic coursework validation, not a complete email verifier.
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_repair(data):
    """Return (cleaned_data, field_errors) without mutating the request JSON."""
    if not isinstance(data, dict):
        return None, {"body": "A JSON object is required"}

    cleaned = {}
    errors = {}
    for field, max_length in FIELDS.items():
        raw = data.get(field)
        if not isinstance(raw, str) or not raw.strip():
            errors[field] = "This field is required and must be text"
            continue
        value = raw.strip()
        if len(value) > max_length:
            errors[field] = f"Maximum length is {max_length} characters"
        cleaned[field] = value

    if "email" in cleaned and not EMAIL_PATTERN.fullmatch(cleaned["email"]):
        errors["email"] = "Provide a valid email address"
    if "service_type" in cleaned and cleaned["service_type"] not in SERVICE_TYPES:
        errors["service_type"] = "Choose Basic, Standard, Deluxe or Other"

    return cleaned, errors
