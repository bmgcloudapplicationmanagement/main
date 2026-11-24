"""API contract tests for Person 2. All records use fictional test data."""

import pytest


def test_health_is_public(client):
    result = client.get("/api/health")
    assert result.status_code == 200
    assert result.json["status"] == "healthy"


def test_create_repair_returns_201_and_id(client, example_request):
    result = client.post("/api/repairs", json=example_request)
    assert result.status_code == 201
    assert isinstance(result.json["id"], int)
    assert result.json["status"] == "Pending"
    assert result.json["created_at"]


def test_list_repairs_after_create(client, example_request, staff_headers):
    client.post("/api/repairs", json=example_request)
    result = client.get("/api/repairs", headers=staff_headers)
    assert result.status_code == 200
    assert len(result.json) == 1
    assert result.json[0]["service_type"] == "Standard"


def test_retrieve_single_repair(client, example_request, staff_headers):
    created = client.post("/api/repairs", json=example_request)
    result = client.get(f"/api/repairs/{created.json['id']}", headers=staff_headers)
    assert result.status_code == 200
    assert result.json["email"] == "customer@example.com"
    assert result.json["status"] == "Pending"


def test_update_repair_status(client, example_request, staff_headers):
    created = client.post("/api/repairs", json=example_request)
    repair_id = created.json["id"]
    updated = client.patch(
        f"/api/repairs/{repair_id}",
        json={"status": "In Progress"},
        headers=staff_headers,
    )
    assert updated.status_code == 200
    assert updated.json["status"] == "In Progress"
    saved = client.get(f"/api/repairs/{repair_id}", headers=staff_headers)
    assert saved.json["status"] == "In Progress"


def test_completing_repair(client, example_request, staff_headers):
    repair_id = client.post("/api/repairs", json=example_request).json["id"]
    result = client.patch(
        f"/api/repairs/{repair_id}",
        json={"status": "Completed"},
        headers=staff_headers,
    )
    assert result.status_code == 200


def test_list_requires_staff_key(client):
    result = client.get("/api/repairs")
    assert result.status_code == 401


def test_retrieve_requires_staff_key(client):
    result = client.get("/api/repairs/1")
    assert result.status_code == 401


def test_update_requires_staff_key(client):
    result = client.patch("/api/repairs/1", json={"status": "Completed"})
    assert result.status_code == 401


def test_wrong_staff_key_is_rejected(client):
    result = client.get("/api/repairs", headers={"X-Staff-Key": "wrong"})
    assert result.status_code == 401


def test_missing_staff_key_config_disables_staff_access(tmp_path):
    from dee_cycles_api import create_app
    application = create_app({
        "TESTING": True,
        "DATABASE_PATH": str(tmp_path / "no_secret.db"),
        "STAFF_API_KEY": "",
    })
    result = application.test_client().get("/api/repairs")
    assert result.status_code == 503


@pytest.mark.parametrize("field", [
    "customer_name", "email", "bicycle_type", "service_type", "description"
])
def test_missing_required_fields(client, example_request, field):
    payload = dict(example_request)
    payload.pop(field)
    response = client.post("/api/repairs", json=payload)
    assert response.status_code == 400
    assert field in response.json["details"]


def test_invalid_service_type(client, example_request):
    example_request["service_type"] = "Nonexistent Tier"
    response = client.post("/api/repairs", json=example_request)
    assert response.status_code == 400
    assert "service_type" in response.json["details"]


def test_invalid_email(client, example_request):
    example_request["email"] = "not-an-email"
    response = client.post("/api/repairs", json=example_request)
    assert response.status_code == 400


def test_blank_description(client, example_request):
    example_request["description"] = "   "
    response = client.post("/api/repairs", json=example_request)
    assert response.status_code == 400


def test_non_json_body(client):
    response = client.post("/api/repairs", data="not JSON", content_type="text/plain")
    assert response.status_code == 400


def test_missing_record_returns_404(client, staff_headers):
    response = client.get("/api/repairs/999999", headers=staff_headers)
    assert response.status_code == 404


def test_update_missing_record_returns_404(client, staff_headers):
    response = client.patch(
        "/api/repairs/999999", json={"status": "Completed"}, headers=staff_headers
    )
    assert response.status_code == 404


def test_invalid_status_rejected(client, example_request, staff_headers):
    repair_id = client.post("/api/repairs", json=example_request).json["id"]
    result = client.patch(
        f"/api/repairs/{repair_id}", json={"status": "Cancelled"}, headers=staff_headers
    )
    assert result.status_code == 400


def test_parameterised_queries_preserve_untrusted_text(client, example_request, staff_headers):
    injected_name = "Robert'); DROP TABLE repair_requests;--"
    example_request["customer_name"] = injected_name
    first = client.post("/api/repairs", json=example_request)
    assert first.status_code == 201
    saved = client.get(f"/api/repairs/{first.json['id']}", headers=staff_headers)
    assert saved.json["customer_name"] == injected_name
    second = client.post("/api/repairs", json=example_request)
    assert second.status_code == 201


def test_payload_size_is_limited(client):
    response = client.post(
        "/api/repairs",
        data="x" * (70 * 1024),
        content_type="application/json",
    )
    assert response.status_code == 413
