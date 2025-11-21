"""
Election Controller

Handles business logic for election-related operations.
"""

from typing import Any, Dict, List, Optional

from app.services import data_service


class ElectionController:
    """Controller for election operations"""

    def __init__(self):
        self.data_service = data_service

    def get_all_elections(self) -> List[Dict[str, Any]]:
        """Get all elections with basic statistics"""
        elections = self.data_service.get_elections()
        result = []

        for election in elections:
            election_data = election.copy()

            # Use efficient statistics method instead of fetching all data
            # This uses COUNT queries instead of loading all records
            stats = self.data_service.get_election_statistics(election["id"])

            election_data["statistics"] = stats

            result.append(election_data)

        return result

    def get_election_by_id(self, election_id: str) -> Optional[Dict[str, Any]]:
        """Get election details with comprehensive statistics"""
        election = self.data_service.get_election(election_id)
        if not election:
            return None

        result = election.copy()

        # Get basic statistics using efficient COUNT queries
        stats = self.data_service.get_election_statistics(election_id)
        
        # Get top parties using efficient SQL GROUP BY query
        top_parties = self.data_service.get_party_seat_counts(election_id, limit=5)

        result["statistics"] = {
            **stats,
            "top_parties": top_parties,
        }

        return result
