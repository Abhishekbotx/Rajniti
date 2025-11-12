"""
Database Data Service Implementation

Reads data from the database using SQLAlchemy models.
Works with both local PostgreSQL and Supabase.
"""

from typing import Any, Dict, List, Optional

from app.database import get_db_session
from app.database.models import Candidate as DbCandidate
from app.database.models import Constituency as DbConstituency
from app.database.models import Party as DbParty
from app.models import Constituency, Election, ElectionType, Party

from .data_service import DataService


class DbDataService(DataService):
    """Database-backed data service implementation"""

    def __init__(self):
        # For now, we'll support Lok Sabha 2024 similar to JSON service
        # This can be extended to support multiple elections from the database
        self._elections_cache = None

    def get_elections(self) -> List[Election]:
        """Get all available elections"""
        if self._elections_cache is None:
            # TODO: Store elections metadata in database
            # For now, return hardcoded Lok Sabha 2024
            self._elections_cache = [
                Election(
                    id="lok-sabha-2024",
                    name="Lok Sabha General Elections 2024",
                    type=ElectionType.LOK_SABHA,
                    year=2024,
                )
            ]
        return self._elections_cache

    def get_election(self, election_id: str) -> Optional[Election]:
        """Get a specific election by ID"""
        elections = self.get_elections()
        for election in elections:
            if election.id == election_id:
                return election
        return None

    def get_candidates(self, election_id: str) -> List[Dict[str, Any]]:
        """Get all candidates for an election"""
        if election_id != "lok-sabha-2024":
            return []

        with get_db_session() as session:
            db_candidates = DbCandidate.get_all(session, skip=0, limit=10000)
            # Convert to dict format for API compatibility
            return [self._candidate_to_dict(c, session) for c in db_candidates]

    def get_parties(self, election_id: str) -> List[Party]:
        """Get all parties for an election"""
        if election_id != "lok-sabha-2024":
            return []

        with get_db_session() as session:
            db_parties = DbParty.get_all(session, skip=0, limit=10000)
            # Convert to Pydantic models
            return [
                Party(
                    id=p.id,
                    name=p.name,
                    short_name=p.short_name,
                    symbol=p.symbol,
                )
                for p in db_parties
            ]

    def get_constituencies(self, election_id: str) -> List[Constituency]:
        """Get all constituencies for an election"""
        if election_id != "lok-sabha-2024":
            return []

        with get_db_session() as session:
            db_constituencies = DbConstituency.get_all(session, skip=0, limit=10000)
            # Convert to Pydantic models
            return [
                Constituency(
                    id=c.id,
                    name=c.name,
                    state_id=c.state_id,
                )
                for c in db_constituencies
            ]

    def search_candidates(
        self, query: str, election_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search candidates by name, party, or constituency"""
        if election_id and election_id != "lok-sabha-2024":
            return []

        with get_db_session() as session:
            # Search by name
            db_candidates = DbCandidate.search_by_name(session, query)
            return [self._candidate_to_dict(c, session) for c in db_candidates]

    def get_candidate_by_id(
        self, candidate_id: str, election_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific candidate"""
        if election_id != "lok-sabha-2024":
            return None

        with get_db_session() as session:
            db_candidate = DbCandidate.get_by_id(session, candidate_id)
            if db_candidate:
                return self._candidate_to_dict(db_candidate, session)
            return None

    def get_party_by_name(self, party_name: str, election_id: str) -> Optional[Party]:
        """Get a specific party"""
        if election_id != "lok-sabha-2024":
            return None

        with get_db_session() as session:
            db_party = DbParty.get_by_name(session, party_name)
            if db_party:
                return Party(
                    id=db_party.id,
                    name=db_party.name,
                    short_name=db_party.short_name,
                    symbol=db_party.symbol,
                )
            return None

    def get_constituency_by_id(
        self, constituency_id: str, election_id: str
    ) -> Optional[Constituency]:
        """Get a specific constituency"""
        if election_id != "lok-sabha-2024":
            return None

        with get_db_session() as session:
            db_constituency = DbConstituency.get_by_id(session, constituency_id)
            if db_constituency:
                return Constituency(
                    id=db_constituency.id,
                    name=db_constituency.name,
                    state_id=db_constituency.state_id,
                )
            return None

    def _candidate_to_dict(self, candidate: DbCandidate, session) -> Dict[str, Any]:
        """
        Convert database candidate to dictionary format with enriched data.

        Args:
            candidate: Database candidate model
            session: Database session for fetching related data

        Returns:
            Dictionary with candidate data including party and constituency details
        """
        # Get party details
        party = DbParty.get_by_id(session, candidate.party_id)
        party_name = party.name if party else "Unknown"
        party_short_name = party.short_name if party else "UNK"
        party_symbol = party.symbol if party else ""

        # Get constituency details
        constituency = DbConstituency.get_by_id(session, candidate.constituency_id)
        constituency_name = constituency.name if constituency else "Unknown"
        constituency_state_id = constituency.state_id if constituency else ""

        return {
            "id": candidate.id,
            "name": candidate.name,
            "party_id": candidate.party_id,
            "party_name": party_name,
            "party_short_name": party_short_name,
            "party_symbol": party_symbol,
            "constituency_id": candidate.constituency_id,
            "constituency_name": constituency_name,
            "constituency_state_id": constituency_state_id,
            "state_id": candidate.state_id,
            "status": candidate.status,
            "type": candidate.type,
            "image_url": candidate.image_url,
            "election_id": "lok-sabha-2024",
        }
