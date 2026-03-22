import importlib
import sys
import types
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_firestore(monkeypatch):
    """Mock firebase.db before app import so tests never hit real Firebase."""
    mock_db = MagicMock(name="mock_db")
    mock_collection = MagicMock(name="mock_collection")
    mock_doc_ref = MagicMock(name="mock_doc_ref")
    mock_snapshot = MagicMock(name="mock_snapshot")

    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_doc_ref
    mock_doc_ref.get.return_value = mock_snapshot

    mock_snapshot.exists = True
    mock_snapshot.to_dict.return_value = {
        "first_name": "Test",
        "last_name": "User",
        "student_id": "12345678",
    }

    fake_firebase_module = types.ModuleType("firebase")
    fake_firebase_module.db = mock_db
    monkeypatch.setitem(sys.modules, "firebase", fake_firebase_module)

    # Force a fresh import path so modules pick up mocked firebase
    for module_name in [
        "app",
        "blueprints.api",
        "blueprints.api.routes",
        "blueprints.auth",
        "blueprints.auth.routes",
        "blueprints.dashboard",
        "blueprints.dashboard.routes",
        "blueprints.profile",
        "blueprints.profile.routes",
        "utils.profile",
    ]:
        sys.modules.pop(module_name, None)

    return {
        "db": mock_db,
        "collection": mock_collection,
        "doc_ref": mock_doc_ref,
        "snapshot": mock_snapshot,
    }


@pytest.fixture
def client(monkeypatch, mock_firestore):
    """Flask test client with TESTING enabled."""
    monkeypatch.setenv("SENSOR_API_KEY", "test-sensor-key")

    app_module = importlib.import_module("app")
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as test_client:
        yield test_client


@pytest.fixture
def mock_firebase_auth(monkeypatch):
    """Mock JWT verification to return a known uid."""
    verify_mock = MagicMock(return_value={"uid": "test_user_123"})
    monkeypatch.setattr("decorators.auth.auth.verify_id_token", verify_mock)
    return verify_mock