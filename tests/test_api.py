import pytest
import json
from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


# --- Health Check ---

def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data


# --- POST /analyze ---

def test_analyze_missing_body(client):
    res = client.post("/api/v1/analyze", content_type="application/json")
    assert res.status_code == 400


def test_analyze_missing_url(client):
    res = client.post("/api/v1/analyze",
                      data=json.dumps({}),
                      content_type="application/json")
    assert res.status_code == 400


def test_analyze_empty_url(client):
    res = client.post("/api/v1/analyze",
                      data=json.dumps({"url": ""}),
                      content_type="application/json")
    assert res.status_code == 400


def test_analyze_invalid_url(client):
    res = client.post("/api/v1/analyze",
                      data=json.dumps({"url": "not-a-real-url-xyz123"}),
                      content_type="application/json")
    assert res.status_code == 422
    data = res.get_json()
    assert data["success"] is False


def test_analyze_url_too_long(client):
    res = client.post("/api/v1/analyze",
                      data=json.dumps({"url": "https://" + "a" * 2050}),
                      content_type="application/json")
    assert res.status_code == 400


# --- GET /analyze ---

def test_analyze_get_missing_param(client):
    res = client.get("/api/v1/analyze")
    assert res.status_code == 400


def test_analyze_get_invalid_url(client):
    res = client.get("/api/v1/analyze?url=not-a-real-site-xyz")
    assert res.status_code == 422


# --- 404 ---

def test_404(client):
    res = client.get("/api/v1/nonexistent")
    assert res.status_code == 404
    data = res.get_json()
    assert data["success"] is False
