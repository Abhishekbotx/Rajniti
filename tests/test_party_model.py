"""
Tests for Party database model.
"""

import pytest

from app.database import get_db_session, init_db
from app.database.models import Party


@pytest.fixture(scope="module")
def setup_database():
    """Setup test database."""
    init_db()
    yield
    # Cleanup after tests
    # Note: In a real test setup, you'd use a separate test database


@pytest.fixture
def clean_session():
    """Get a clean database session for each test."""
    with get_db_session() as session:
        yield session
        # Rollback any changes made in the test
        session.rollback()


def test_party_create(setup_database, clean_session):
    """Test creating a party."""
    party = Party.create(
        session=clean_session,
        id="test-1",
        name="Test Party",
        short_name="TP",
        symbol="Test Symbol",
    )

    assert party.id == "test-1"
    assert party.name == "Test Party"
    assert party.short_name == "TP"
    assert party.symbol == "Test Symbol"


def test_party_get_by_id(setup_database, clean_session):
    """Test getting a party by ID."""
    # Create a party
    Party.create(
        session=clean_session,
        id="test-2",
        name="Test Party 2",
        short_name="TP2",
        symbol="",
    )

    # Retrieve it
    party = Party.get_by_id(clean_session, "test-2")
    assert party is not None
    assert party.name == "Test Party 2"


def test_party_get_by_name(setup_database, clean_session):
    """Test getting a party by name."""
    # Create a party
    Party.create(
        session=clean_session,
        id="test-3",
        name="Unique Party Name",
        short_name="UPN",
        symbol="",
    )

    # Retrieve it
    party = Party.get_by_name(clean_session, "Unique Party Name")
    assert party is not None
    assert party.id == "test-3"


def test_party_update(setup_database, clean_session):
    """Test updating a party."""
    # Create a party
    party = Party.create(
        session=clean_session,
        id="test-4",
        name="Old Name",
        short_name="ON",
        symbol="Old Symbol",
    )

    # Update it
    party.update(clean_session, name="New Name", symbol="New Symbol")

    # Verify update
    updated_party = Party.get_by_id(clean_session, "test-4")
    assert updated_party.name == "New Name"
    assert updated_party.symbol == "New Symbol"
    assert updated_party.short_name == "ON"  # Unchanged


def test_party_bulk_create(setup_database, clean_session):
    """Test bulk creating parties."""
    parties_data = [
        {"id": "bulk-1", "name": "Bulk Party 1", "short_name": "BP1", "symbol": ""},
        {"id": "bulk-2", "name": "Bulk Party 2", "short_name": "BP2", "symbol": ""},
        {"id": "bulk-3", "name": "Bulk Party 3", "short_name": "BP3", "symbol": ""},
    ]

    parties = Party.bulk_create(clean_session, parties_data)

    assert len(parties) == 3

    # Verify they were created
    party1 = Party.get_by_id(clean_session, "bulk-1")
    assert party1 is not None
    assert party1.name == "Bulk Party 1"
