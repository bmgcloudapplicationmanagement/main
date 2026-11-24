"""Test isolation: every test receives a disposable SQLite database."""

import pytest

from dee_cycles_api import create_app


@pytest.fixture
def app(tmp_path):
    application = create_app({
        "TESTING": True,
        "DATABASE_PATH": str(tmp_path / "test_repairs.db"),
        "STAFF_API_KEY": "test-only-staff-key",
    })
    yield application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def staff_headers():
    return {"X-Staff-Key": "test-only-staff-key"}


@pytest.fixture
def example_request():
    return {
        "customer_name": "Example Customer",
        "email": "customer@example.com",
        "bicycle_type": "Road Bike",
        "service_type": "Standard",
        "description": "Brake adjustment and chain inspection",
    }
