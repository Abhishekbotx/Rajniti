"""
Tests for Candidate database model.
"""

import pytest

from app.database import get_db_session, init_db
from app.database.models import Candidate


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


def test_candidate_create(setup_database, clean_session):
    """Test creating a candidate."""
    cand = Candidate.create(
        session=clean_session,
        id="test-cand-1",
        name="Test Candidate",
        party_id="party-1",
        constituency_id="const-1",
        state_id="TS",
        status="WON",
        type="MP",
        image_url="https://example.com/image.jpg",
    )

    assert cand.id == "test-cand-1"
    assert cand.name == "Test Candidate"
    assert cand.party_id == "party-1"
    assert cand.status == "WON"


def test_candidate_get_by_id(setup_database, clean_session):
    """Test getting a candidate by ID."""
    Candidate.create(
        session=clean_session,
        id="test-cand-2",
        name="Test Candidate 2",
        party_id="party-1",
        constituency_id="const-1",
        state_id="TS",
        status="LOST",
    )

    cand = Candidate.get_by_id(clean_session, "test-cand-2")
    assert cand is not None
    assert cand.name == "Test Candidate 2"


def test_candidate_get_by_party(setup_database, clean_session):
    """Test getting candidates by party."""
    Candidate.create(clean_session, "cand-p-1", "Cand 1", "party-x", "c-1", "S1", "WON")
    Candidate.create(
        clean_session, "cand-p-2", "Cand 2", "party-x", "c-2", "S1", "LOST"
    )
    Candidate.create(clean_session, "cand-p-3", "Cand 3", "party-y", "c-3", "S1", "WON")

    party_x_cands = Candidate.get_by_party(clean_session, "party-x")
    assert len(party_x_cands) >= 2


def test_candidate_get_winners(setup_database, clean_session):
    """Test getting winning candidates."""
    Candidate.create(clean_session, "cand-w-1", "Winner 1", "p-1", "c-1", "S1", "WON")
    Candidate.create(clean_session, "cand-w-2", "Loser 1", "p-1", "c-2", "S1", "LOST")
    Candidate.create(clean_session, "cand-w-3", "Winner 2", "p-2", "c-3", "S1", "WON")

    winners = Candidate.get_winners(clean_session, skip=0, limit=100)
    assert len(winners) >= 2
    assert all(w.status == "WON" for w in winners)


def test_candidate_search_by_name(setup_database, clean_session):
    """Test searching candidates by name."""
    Candidate.create(clean_session, "cand-s-1", "John Doe", "p-1", "c-1", "S1", "WON")
    Candidate.create(clean_session, "cand-s-2", "Jane Doe", "p-1", "c-2", "S1", "LOST")
    Candidate.create(clean_session, "cand-s-3", "Bob Smith", "p-2", "c-3", "S1", "WON")

    # Search for "Doe"
    results = Candidate.search_by_name(clean_session, "Doe")
    assert len(results) >= 2

    # Search for "John"
    results = Candidate.search_by_name(clean_session, "John")
    assert len(results) >= 1


def test_candidate_bulk_create(setup_database, clean_session):
    """Test bulk creating candidates."""
    cands_data = [
        {
            "id": "bulk-cand-1",
            "name": "Bulk 1",
            "party_id": "p-1",
            "constituency_id": "c-1",
            "state_id": "S1",
            "status": "WON",
        },
        {
            "id": "bulk-cand-2",
            "name": "Bulk 2",
            "party_id": "p-2",
            "constituency_id": "c-2",
            "state_id": "S1",
            "status": "LOST",
        },
    ]

    cands = Candidate.bulk_create(clean_session, cands_data)
    assert len(cands) == 2

    cand1 = Candidate.get_by_id(clean_session, "bulk-cand-1")
    assert cand1 is not None
    assert cand1.name == "Bulk 1"
