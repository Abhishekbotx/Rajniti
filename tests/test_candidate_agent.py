"""
Tests for the Candidate Data Population Agent.
"""

import sys
from unittest.mock import Mock, patch
import pytest

# Mock chromadb before any imports to avoid numpy compatibility issues in tests
sys.modules['chromadb'] = Mock()
sys.modules['chromadb.config'] = Mock()

from app.database.models import Candidate
from app.services.candidate_agent import CandidateDataAgent


@pytest.fixture
def mock_perplexity_service():
    """Mock Perplexity service for testing."""
    with patch("app.services.candidate_agent.PerplexityService") as mock:
        service = Mock()
        mock.return_value = service
        yield service


@pytest.fixture
def agent(mock_perplexity_service):
    """Create a CandidateDataAgent instance for testing."""
    # Disable vector DB for tests to avoid initialization issues
    return CandidateDataAgent(perplexity_api_key="test-key", enable_vector_db=False)


@pytest.fixture
def mock_candidate():
    """Create a mock candidate for testing."""
    candidate = Mock(spec=Candidate)
    candidate.id = "test-123"
    candidate.name = "Test Candidate"
    candidate.constituency_id = "DL-1"
    candidate.education_background = None
    candidate.political_background = None
    candidate.family_background = None
    candidate.assets = None
    candidate.liabilities = None
    candidate.crime_cases = None
    candidate.update = Mock()
    return candidate


def test_agent_initialization(mock_perplexity_service):
    """Test that the agent initializes correctly."""
    agent = CandidateDataAgent(perplexity_api_key="test-key", enable_vector_db=False)
    assert agent is not None
    assert agent.search_service is not None
    assert agent.enable_vector_db is False


def test_create_data_query_education(agent, mock_candidate):
    """Test education query generation."""
    query = agent._create_data_query(mock_candidate, "education")
    assert "Test Candidate" in query
    assert "education background" in query.lower()
    assert "JSON" in query


def test_create_data_query_political(agent, mock_candidate):
    """Test political query generation."""
    query = agent._create_data_query(mock_candidate, "political")
    assert "Test Candidate" in query
    assert "political history" in query.lower()
    assert "elections" in query.lower()


def test_create_data_query_family(agent, mock_candidate):
    """Test family query generation."""
    query = agent._create_data_query(mock_candidate, "family")
    assert "Test Candidate" in query
    assert "family background" in query.lower()
    assert "relation" in query.lower()


def test_create_data_query_assets(agent, mock_candidate):
    """Test assets query generation."""
    query = agent._create_data_query(mock_candidate, "assets")
    assert "Test Candidate" in query
    assert "assets" in query.lower()


def test_extract_json_from_response_valid(agent):
    """Test JSON extraction from valid response."""
    response = 'Some text {"key": "value", "number": 123} more text'
    result = agent._extract_json_from_response(response)
    assert result == {"key": "value", "number": 123}


def test_extract_json_from_response_nested(agent):
    """Test JSON extraction with nested objects."""
    response = 'Text {"person": {"name": "John", "age": 30}} text'
    result = agent._extract_json_from_response(response)
    assert result == {"person": {"name": "John", "age": 30}}


def test_extract_json_from_response_invalid(agent):
    """Test JSON extraction from invalid response."""
    response = "No JSON here at all"
    result = agent._extract_json_from_response(response)
    assert result is None


def test_extract_json_from_response_malformed(agent):
    """Test JSON extraction from malformed JSON."""
    response = '{"incomplete": "json"'
    result = agent._extract_json_from_response(response)
    assert result is None


def test_fetch_education_background_success(
    agent, mock_candidate, mock_perplexity_service
):
    """Test successful education background fetch."""
    mock_perplexity_service.search_india.return_value = {
        "answer": '{"year": "2000", "stream": "Political Science", "college": "Delhi University"}',
        "error": None,
    }

    result = agent.fetch_education_background(mock_candidate)

    assert result is not None
    assert result[0]["year"] == "2000"
    assert result[0]["stream"] == "Political Science"


def test_fetch_education_background_error(
    agent, mock_candidate, mock_perplexity_service
):
    """Test education background fetch with API error."""
    mock_perplexity_service.search_india.return_value = {
        "answer": "",
        "error": "API Error",
    }

    result = agent.fetch_education_background(mock_candidate)
    assert result is None


def test_fetch_political_background_success(
    agent, mock_candidate, mock_perplexity_service
):
    """Test successful political background fetch."""
    mock_perplexity_service.search_india.return_value = {
        "answer": '[{"election_year": "2019", "party": "ABC", "result": "WON", "constituency": "Delhi"}]',
        "error": None,
    }

    result = agent.fetch_political_background(mock_candidate)

    assert result is not None
    assert len(result) == 1
    assert result[0]["party"] == "ABC"


def test_fetch_family_background_success(
    agent, mock_candidate, mock_perplexity_service
):
    """Test successful family background fetch."""
    mock_perplexity_service.search_india.return_value = {
        "answer": '[{"name": "Father Name", "profession": "Businessman", "relation": "Father"}]',
        "error": None,
    }

    result = agent.fetch_family_background(mock_candidate)

    assert result is not None
    assert result[0]["relation"] == "Father"


def test_fetch_assets_success(agent, mock_candidate, mock_perplexity_service):
    """Test successful assets fetch."""
    mock_perplexity_service.search_india.return_value = {
        "answer": '[{"type": "CASH", "amount": 5000000.0, "description": "Cash in hand", "owned_by": "SELF"}]',
        "error": None,
    }

    result = agent.fetch_assets(mock_candidate)

    assert result is not None
    assert result[0]["type"] == "CASH"


def test_populate_candidate_data_all_fields(
    agent, mock_candidate, mock_perplexity_service
):
    """Test populating all candidate data fields."""
    # Mock successful responses for all fields
    mock_perplexity_service.search_india.side_effect = [
        {
            "answer": '{"year": "2000", "stream": "Political Science"}',
            "error": None,
        },
        {"answer": '[{"election_year": "2019", "party": "BJP"}]', "error": None},
        {"answer": '[{"name": "Test Father", "relation": "Father"}]', "error": None},
        {"answer": '[{"type": "CASH", "amount": 0.0}]', "error": None},
        {"answer": '[{"type": "LOAN", "amount": 0.0}]', "error": None},
        {"answer": '[{"fir_no": "123", "charges_framed": false}]', "error": None},
    ]

    mock_session = Mock()
    mock_session.commit = Mock()

    with patch("time.sleep"):  # Skip delays in tests
        status = agent.populate_candidate_data(
            mock_session, mock_candidate, delay_between_requests=0
        )

    assert status["education"] is True
    assert status["political"] is True
    assert status["family"] is True
    assert status["assets"] is True
    assert status["liabilities"] is True
    assert status["crime_cases"] is True

    # Verify update was called
    mock_candidate.update.assert_called_once()


def test_populate_candidate_data_partial_fields(
    agent, mock_candidate, mock_perplexity_service
):
    """Test populating only some candidate data fields."""
    # Mock successful response for education, failed for others
    mock_perplexity_service.search_india.side_effect = [
        {"answer": '{"year": "2000"}', "error": None},
        {"answer": "No data found", "error": None},  # No JSON
        {"answer": "No data found", "error": None},
        {"answer": "No data found", "error": None},
        {"answer": "No data found", "error": None},
        {"answer": "No data found", "error": None},
    ]

    mock_session = Mock()

    with patch("time.sleep"):
        status = agent.populate_candidate_data(
            mock_session, mock_candidate, delay_between_requests=0
        )

    assert status["education"] is True
    assert status["political"] is False
    assert status["family"] is False
    assert status["assets"] is False


def test_populate_candidate_data_skip_existing(
    agent, mock_candidate, mock_perplexity_service
):
    """Test that existing data is not overwritten."""
    # Set some existing data
    mock_candidate.education_background = {"existing": "data"}

    mock_session = Mock()

    with patch("time.sleep"):
        status = agent.populate_candidate_data(
            mock_session, mock_candidate, delay_between_requests=0
        )

    # Should mark as successful without fetching
    assert status["education"] is True
    # Should not call Perplexity for education (already exists)
    # Only 5 calls for political, family, assets, liabilities, crime_cases
    assert mock_perplexity_service.search_india.call_count <= 5


def test_find_candidates_needing_data():
    """Test finding candidates that need data."""
    mock_session = Mock()
    mock_query = Mock()
    mock_filter = Mock()
    mock_limit = Mock()

    # Setup mock chain
    mock_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.limit.return_value = mock_limit
    mock_limit.all.return_value = [Mock(spec=Candidate), Mock(spec=Candidate)]

    agent = CandidateDataAgent(perplexity_api_key="test-key", enable_vector_db=False)

    candidates = agent.find_candidates_needing_data(mock_session, limit=10)

    assert len(candidates) == 2
    mock_session.query.assert_called_once_with(Candidate)


def test_run_agent_no_candidates():
    """Test agent run when no candidates need data."""
    mock_session = Mock()
    mock_query = Mock()
    mock_filter = Mock()
    mock_limit = Mock()

    mock_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.limit.return_value = mock_limit
    mock_limit.all.return_value = []

    agent = CandidateDataAgent(perplexity_api_key="test-key", enable_vector_db=False)

    stats = agent.run(mock_session, batch_size=10)

    assert stats["total_processed"] == 0
    assert stats["successful"] == 0
    assert stats["partial"] == 0
    assert stats["failed"] == 0
