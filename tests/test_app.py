"""
Unit tests for app.py — run by the 'Test' stage of the Jenkins pipeline.
"""

import os
import sys

# Allow importing app.py from the ../app folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app  # noqa: E402


def get_client():
    app.testing = True
    return app.test_client()


def test_index():
    client = get_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Simple DevOps demo app is running!"


def test_health():
    client = get_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_add_success():
    client = get_client()
    resp = client.get("/add?a=2&b=3")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 5.0


def test_add_invalid_input():
    client = get_client()
    resp = client.get("/add?a=foo&b=3")
    assert resp.status_code == 400
    assert "error" in resp.get_json()
