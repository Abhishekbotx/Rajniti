"""
Tests for the Vector DB Pipeline service.
"""

import sys
from unittest.mock import Mock, patch, MagicMock
import pytest

# Mock chromadb before importing to avoid numpy compatibility issues in tests
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()

from app.services.vector_db_pipeline import VectorDBPipeline


# Now we can import Candidate after mocking chromadb
from app.database.models import Candidate


@pytest.fixture
def mock_vector_db_service():
    """Mock VectorDBService for testing."""
    with patch("app.services.vector_db_pipeline.VectorDBService") as mock:
        service = Mock()
        mock.return_value = service
        service.upsert_candidate_data = Mock()
        service.delete_candidate = Mock()
        service.count_candidates = Mock(return_value=100)
        yield service


@pytest.fixture
def pipeline(mock_vector_db_service):
    """Create a VectorDBPipeline instance for testing."""
    return VectorDBPipeline()


@pytest.fixture
def mock_candidate():
    """Create a mock candidate for testing."""
    candidate = Mock(spec=Candidate)
    candidate.id = "test-123"
    candidate.name = "Test Candidate"
    candidate.party_id = "BJP"
    candidate.constituency_id = "DL-1"
    candidate.state_id = "DL"
    candidate.status = "WON"
    candidate.type = "MLA"
    candidate.image_url = "https://example.com/image.jpg"
    candidate.education_background = [
        {"year": "2000", "college": "Delhi University", "stream": "Political Science"}
    ]
    candidate.political_background = [
        {
            "election_year": "2019",
            "party": "BJP",
            "constituency": "Delhi-1",
            "result": "WON",
            "position": "MLA",
        }
    ]
    candidate.family_background = [
        {"name": "Father Name", "relation": "Father", "profession": "Businessman"}
    ]
    candidate.assets = [
        {"type": "CASH", "amount": 1000000.0, "description": "Cash in hand", "owned_by": "SELF"}
    ]
    candidate.liabilities = [
        {"type": "LOAN", "amount": 500000.0, "description": "Home loan", "owned_by": "SELF"}
    ]
    candidate.crime_cases = [
        {"fir_no": "123", "charges_framed": False, "description": "Pending case"}
    ]
    return candidate


def test_pipeline_initialization(mock_vector_db_service):
    """Test that the pipeline initializes correctly."""
    pipeline = VectorDBPipeline()
    assert pipeline is not None
    assert pipeline.vector_db is not None


def test_candidate_to_text_basic(pipeline, mock_candidate):
    """Test converting candidate to text format."""
    text = pipeline._candidate_to_text(mock_candidate)
    
    assert "Test Candidate" in text
    assert "DL-1" in text
    assert "BJP" in text
    assert "WON" in text
    assert "MLA" in text


def test_candidate_to_text_with_education(pipeline, mock_candidate):
    """Test text includes education information."""
    text = pipeline._candidate_to_text(mock_candidate)
    
    assert "Education:" in text
    assert "2000" in text
    assert "Delhi University" in text
    assert "Political Science" in text


def test_candidate_to_text_with_political_history(pipeline, mock_candidate):
    """Test text includes political history."""
    text = pipeline._candidate_to_text(mock_candidate)
    
    assert "Political History:" in text
    assert "2019" in text
    assert "won" in text.lower()


def test_candidate_to_text_with_family(pipeline, mock_candidate):
    """Test text includes family information."""
    text = pipeline._candidate_to_text(mock_candidate)
    
    assert "Family:" in text
    assert "Father Name" in text
    assert "Businessman" in text


def test_candidate_to_text_with_assets(pipeline, mock_candidate):
    """Test text includes assets information."""
    text = pipeline._candidate_to_text(mock_candidate)
    
    assert "Assets:" in text
    assert "₹1,000,000.00" in text


def test_candidate_to_text_with_crime_cases(pipeline, mock_candidate):
    """Test text includes crime cases information."""
    text = pipeline._candidate_to_text(mock_candidate)
    
    assert "Criminal Cases:" in text
    assert "1 criminal case(s)" in text


def test_candidate_to_text_minimal(pipeline):
    """Test text conversion with minimal candidate data."""
    candidate = Mock(spec=Candidate)
    candidate.id = "min-1"
    candidate.name = "Minimal Candidate"
    candidate.party_id = "INC"
    candidate.constituency_id = "MH-1"
    candidate.state_id = "MH"
    candidate.status = "LOST"
    candidate.type = "MP"
    candidate.image_url = None
    candidate.education_background = None
    candidate.political_background = None
    candidate.family_background = None
    candidate.assets = None
    candidate.liabilities = None
    candidate.crime_cases = None
    
    text = pipeline._candidate_to_text(candidate)
    
    assert "Minimal Candidate" in text
    assert "INC" in text
    assert "LOST" in text
    # Should not contain optional fields
    assert "Education:" not in text
    assert "Political History:" not in text


def test_candidate_to_metadata(pipeline, mock_candidate):
    """Test extracting metadata from candidate."""
    metadata = pipeline._candidate_to_metadata(mock_candidate)
    
    assert metadata["candidate_id"] == "test-123"
    assert metadata["name"] == "Test Candidate"
    assert metadata["party_id"] == "BJP"
    assert metadata["state_id"] == "DL"
    assert metadata["status"] == "WON"
    assert metadata["type"] == "MLA"
    assert metadata["image_url"] == "https://example.com/image.jpg"
    assert metadata["education_count"] == 1
    assert metadata["political_history_count"] == 1
    assert metadata["family_members_count"] == 1
    assert metadata["assets_count"] == 1
    assert metadata["crime_cases_count"] == 1


def test_candidate_to_metadata_minimal(pipeline):
    """Test metadata extraction with minimal data."""
    candidate = Mock(spec=Candidate)
    candidate.id = "min-1"
    candidate.name = "Minimal"
    candidate.party_id = "INC"
    candidate.constituency_id = "MH-1"
    candidate.state_id = "MH"
    candidate.status = "LOST"
    candidate.type = "MP"
    candidate.image_url = None
    candidate.education_background = None
    candidate.political_background = None
    candidate.family_background = None
    candidate.assets = None
    candidate.liabilities = None
    candidate.crime_cases = None
    
    metadata = pipeline._candidate_to_metadata(candidate)
    
    assert "education_count" not in metadata
    assert "political_history_count" not in metadata


def test_sync_candidate_success(pipeline, mock_candidate, mock_vector_db_service):
    """Test successful candidate sync."""
    result = pipeline.sync_candidate(mock_candidate)
    
    assert result is True
    mock_vector_db_service.upsert_candidate_data.assert_called_once()
    
    # Check the call arguments
    call_args = mock_vector_db_service.upsert_candidate_data.call_args
    assert call_args[1]["candidate_id"] == "test-123"
    assert "Test Candidate" in call_args[1]["text"]
    assert call_args[1]["metadata"]["name"] == "Test Candidate"


def test_sync_candidate_failure(pipeline, mock_candidate, mock_vector_db_service):
    """Test candidate sync with error."""
    mock_vector_db_service.upsert_candidate_data.side_effect = Exception("Database error")
    
    result = pipeline.sync_candidate(mock_candidate)
    
    assert result is False


def test_sync_candidates_batch(pipeline, mock_vector_db_service):
    """Test batch sync of candidates."""
    mock_session = Mock()
    mock_query = Mock()
    
    # Create mock candidates
    candidates = [
        Mock(spec=Candidate, id=f"test-{i}", name=f"Candidate {i}")
        for i in range(3)
    ]
    for c in candidates:
        c.party_id = "BJP"
        c.constituency_id = "DL-1"
        c.state_id = "DL"
        c.status = "WON"
        c.type = "MLA"
        c.image_url = None
        c.education_background = None
        c.political_background = None
        c.family_background = None
        c.assets = None
        c.liabilities = None
        c.crime_cases = None
    
    # Setup mock chain
    mock_session.query.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = candidates
    
    stats = pipeline.sync_candidates_batch(mock_session, batch_size=10)
    
    assert stats["total"] == 3
    assert stats["synced"] == 3
    assert stats["failed"] == 0
    assert mock_vector_db_service.upsert_candidate_data.call_count == 3


def test_sync_candidates_batch_with_filter(pipeline, mock_vector_db_service):
    """Test batch sync with filter criteria."""
    mock_session = Mock()
    mock_query = Mock()
    
    candidates = [Mock(spec=Candidate, id="test-1", name="Candidate 1")]
    for c in candidates:
        c.party_id = "BJP"
        c.constituency_id = "DL-1"
        c.state_id = "DL"
        c.status = "WON"
        c.type = "MLA"
        c.image_url = None
        c.education_background = None
        c.political_background = None
        c.family_background = None
        c.assets = None
        c.liabilities = None
        c.crime_cases = None
    
    mock_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = candidates
    
    stats = pipeline.sync_candidates_batch(
        mock_session,
        batch_size=10,
        filter_criteria={"status": "WON"}
    )
    
    assert stats["total"] == 1
    mock_query.filter.assert_called()


def test_sync_all_candidates(pipeline, mock_vector_db_service):
    """Test full sync of all candidates."""
    mock_session = Mock()
    mock_query = Mock()
    
    # First batch returns 2 candidates, second batch returns empty
    batch1 = [
        Mock(spec=Candidate, id=f"test-{i}", name=f"Candidate {i}")
        for i in range(2)
    ]
    for c in batch1:
        c.party_id = "BJP"
        c.constituency_id = "DL-1"
        c.state_id = "DL"
        c.status = "WON"
        c.type = "MLA"
        c.image_url = None
        c.education_background = None
        c.political_background = None
        c.family_background = None
        c.assets = None
        c.liabilities = None
        c.crime_cases = None
    
    mock_session.query.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.side_effect = [batch1, []]  # First call returns data, second is empty
    
    stats = pipeline.sync_all_candidates(mock_session, batch_size=10)
    
    assert stats["total"] == 2
    assert stats["synced"] == 2
    assert stats["failed"] == 0
    assert stats["batches"] == 1


def test_delete_candidate_success(pipeline, mock_vector_db_service):
    """Test successful candidate deletion."""
    result = pipeline.delete_candidate("test-123")
    
    assert result is True
    mock_vector_db_service.delete_candidate.assert_called_once_with("test-123")


def test_delete_candidate_failure(pipeline, mock_vector_db_service):
    """Test candidate deletion with error."""
    mock_vector_db_service.delete_candidate.side_effect = Exception("Delete error")
    
    result = pipeline.delete_candidate("test-123")
    
    assert result is False
