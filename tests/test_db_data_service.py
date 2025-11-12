"""
Tests for Database Data Service.
"""

import pytest

from app.database import get_db_session, init_db
from app.database.models import Candidate, Constituency, Party
from app.services.db_data_service import DbDataService


@pytest.fixture(scope="module")
def setup_database():
    """Setup test database."""
    init_db()
    yield


@pytest.fixture
def setup_test_data(setup_database):
    """Setup test data in database."""
    with get_db_session() as session:
        # Create test parties
        Party.create(session, "test-party-1", "Test Party 1", "TP1", "Symbol1")
        Party.create(session, "test-party-2", "Test Party 2", "TP2", "Symbol2")

        # Create test constituencies
        Constituency.create(session, "test-const-1", "Test Constituency 1", "TC")
        Constituency.create(session, "test-const-2", "Test Constituency 2", "TC")

        # Create test candidates
        Candidate.create(
            session,
            "test-cand-1",
            "John Doe",
            "test-party-1",
            "test-const-1",
            "TC",
            "WON",
            "MP",
        )
        Candidate.create(
            session,
            "test-cand-2",
            "Jane Smith",
            "test-party-2",
            "test-const-2",
            "TC",
            "LOST",
            "MP",
        )

    yield

    # Cleanup
    with get_db_session() as session:
        session.rollback()


def test_db_service_get_elections(setup_test_data):
    """Test getting elections from database service."""
    service = DbDataService()
    elections = service.get_elections()

    assert len(elections) > 0
    assert elections[0].id == "lok-sabha-2024"


def test_db_service_get_parties(setup_test_data):
    """Test getting parties from database service."""
    service = DbDataService()
    parties = service.get_parties("lok-sabha-2024")

    assert len(parties) >= 2
    party_names = [p.name for p in parties]
    assert "Test Party 1" in party_names


def test_db_service_get_constituencies(setup_test_data):
    """Test getting constituencies from database service."""
    service = DbDataService()
    constituencies = service.get_constituencies("lok-sabha-2024")

    assert len(constituencies) >= 2
    const_names = [c.name for c in constituencies]
    assert "Test Constituency 1" in const_names


def test_db_service_get_candidates(setup_test_data):
    """Test getting candidates from database service."""
    service = DbDataService()
    candidates = service.get_candidates("lok-sabha-2024")

    assert len(candidates) >= 2
    candidate_names = [c["name"] for c in candidates]
    assert "John Doe" in candidate_names


def test_db_service_search_candidates(setup_test_data):
    """Test searching candidates."""
    service = DbDataService()

    # Search for "John"
    results = service.search_candidates("John")
    assert len(results) >= 1
    assert results[0]["name"] == "John Doe"


def test_db_service_get_candidate_by_id(setup_test_data):
    """Test getting candidate by ID."""
    service = DbDataService()
    candidate = service.get_candidate_by_id("test-cand-1", "lok-sabha-2024")

    assert candidate is not None
    assert candidate["name"] == "John Doe"
    assert candidate["party_name"] == "Test Party 1"
    assert candidate["constituency_name"] == "Test Constituency 1"


def test_db_service_get_party_by_name(setup_test_data):
    """Test getting party by name."""
    service = DbDataService()
    party = service.get_party_by_name("Test Party 1", "lok-sabha-2024")

    assert party is not None
    assert party.name == "Test Party 1"
    assert party.short_name == "TP1"


def test_db_service_get_constituency_by_id(setup_test_data):
    """Test getting constituency by ID."""
    service = DbDataService()
    const = service.get_constituency_by_id("test-const-1", "lok-sabha-2024")

    assert const is not None
    assert const.name == "Test Constituency 1"
    assert const.state_id == "TC"
