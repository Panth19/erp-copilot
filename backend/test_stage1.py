"""
Stage 1 verification suite. Run with: python3 -m pytest test_stage1.py -v
Uses FastAPI's TestClient so no live server is needed.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ---------- Step 6: login endpoint ----------
def test_login_correct_clerk_credentials():
    r = client.post("/auth/login", json={"username": "clerk", "password": "clerk123"})
    assert r.status_code == 200
    assert r.json()["role"] == "clerk"
    assert "access_token" in r.cookies


def test_login_correct_manager_credentials():
    r = client.post("/auth/login", json={"username": "manager", "password": "manager123"})
    assert r.status_code == 200
    assert r.json()["role"] == "manager"
    assert "access_token" in r.cookies


def test_login_wrong_password_rejected():
    r = client.post("/auth/login", json={"username": "clerk", "password": "nope"})
    assert r.status_code == 401


def test_login_unknown_user_rejected():
    r = client.post("/auth/login", json={"username": "ghost", "password": "whatever"})
    assert r.status_code == 401


def test_login_missing_fields_rejected():
    r = client.post("/auth/login", json={"username": "clerk"})
    assert r.status_code == 422  # pydantic validation catches missing password


# ---------- Step 7: auth dependency enforcement ----------
def test_invoices_requires_auth():
    anon_client = TestClient(app)  # no cookies
    r = anon_client.get("/invoices")
    assert r.status_code == 401


def test_invoices_accessible_when_logged_in():
    r = client.post("/auth/login", json={"username": "clerk", "password": "clerk123"})
    assert r.status_code == 200
    r2 = client.get("/invoices")
    assert r2.status_code == 200


# ---------- Step 8: invoices filtering ----------
def test_list_all_invoices_returns_75():
    client.post("/auth/login", json={"username": "clerk", "password": "clerk123"})
    r = client.get("/invoices")
    assert r.status_code == 200
    assert len(r.json()) == 75


def test_filter_invoices_by_status():
    client.post("/auth/login", json={"username": "clerk", "password": "clerk123"})
    r = client.get("/invoices", params={"status": "overdue"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    assert all(inv["status"] == "overdue" for inv in data)


def test_filter_invoices_by_date_range():
    client.post("/auth/login", json={"username": "clerk", "password": "clerk123"})
    r = client.get("/invoices", params={"start_date": "2026-01-01", "end_date": "2026-01-31"})
    assert r.status_code == 200
    for inv in r.json():
        assert "2026-01" in inv["date"]


def test_filter_invoices_bad_date_returns_422():
    client.post("/auth/login", json={"username": "clerk", "password": "clerk123"})
    r = client.get("/invoices", params={"start_date": "not-a-date"})
    assert r.status_code == 422


def test_filter_invoices_by_vendor_name_partial_match():
    client.post("/auth/login", json={"username": "clerk", "password": "clerk123"})
    r = client.get("/invoices", params={"vendor": "Nova Electronics"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    assert all("nova electronics" in inv["vendor_name"].lower() for inv in data)


# ---------- Step 9: approvals RBAC ----------
def test_approvals_pending_forbidden_for_clerk():
    client.post("/auth/login", json={"username": "clerk", "password": "clerk123"})
    r = client.get("/approvals/pending")
    assert r.status_code == 403


def test_approvals_pending_allowed_for_manager():
    client.post("/auth/login", json={"username": "manager", "password": "manager123"})
    r = client.get("/approvals/pending")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert all(a["status"] == "pending" for a in data)


def test_approvals_pending_requires_auth():
    anon_client = TestClient(app)
    r = anon_client.get("/approvals/pending")
    assert r.status_code == 401


# ---------- Step 10: general error handling ----------
def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_logout_clears_cookie():
    client.post("/auth/login", json={"username": "manager", "password": "manager123"})
    r = client.post("/auth/logout")
    assert r.status_code == 200
    r2 = client.get("/approvals/pending")
    assert r2.status_code == 401
