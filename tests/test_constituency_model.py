"""
Tests for Constituency database model.
"""

import pytest

from app.database import get_db_session, init_db
from app.database.models import Constituency


@pytest.fixture(scope="module")
def setup_database():
    """Setup test database."""
    init_db()
    yield


@pytest.fixture
def clean_session():
    """Get a clean database session for each test."""
    with get_db_session() as session:
        yield session
        session.rollback()


def test_constituency_create(setup_database, clean_session):
    """Test creating a constituency."""
    const = Constituency.create(
        session=clean_session,
        id="test-const-1",
        name="Test Constituency",
        state_id="TS",
    )

    assert const.id == "test-const-1"
    assert const.name == "Test Constituency"
    assert const.state_id == "TS"


def test_constituency_get_by_id(setup_database, clean_session):
    """Test getting a constituency by ID."""
    Constituency.create(
        session=clean_session,
        id="test-const-2",
        name="Test Constituency 2",
        state_id="TS",
    )

    const = Constituency.get_by_id(clean_session, "test-const-2")
    assert const is not None
    assert const.name == "Test Constituency 2"


def test_constituency_get_by_state(setup_database, clean_session):
    """Test getting constituencies by state."""
    # Create multiple constituencies
    Constituency.create(clean_session, "state-1", "Const 1", "DL")
    Constituency.create(clean_session, "state-2", "Const 2", "DL")
    Constituency.create(clean_session, "state-3", "Const 3", "MH")

    # Get by state
    dl_consts = Constituency.get_by_state(clean_session, "DL")
    assert len(dl_consts) >= 2

    mh_consts = Constituency.get_by_state(clean_session, "MH")
    assert len(mh_consts) >= 1


def test_constituency_bulk_create(setup_database, clean_session):
    """Test bulk creating constituencies."""
    consts_data = [
        {"id": "bulk-c-1", "name": "Bulk Const 1", "state_id": "BC"},
        {"id": "bulk-c-2", "name": "Bulk Const 2", "state_id": "BC"},
    ]

    consts = Constituency.bulk_create(clean_session, consts_data)
    assert len(consts) == 2

    const1 = Constituency.get_by_id(clean_session, "bulk-c-1")
    assert const1 is not None
    assert const1.name == "Bulk Const 1"
