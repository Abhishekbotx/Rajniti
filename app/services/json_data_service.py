"""
JSON Data Service Implementation - Lok Sabha Only

Reads data from existing JSON files in the app/data directory.
Optimized for Lok Sabha 2024 election data.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.models import Constituency, Election, ElectionType, Party

from .data_service import DataService

class JsonDataService(DataService):
    """JSON file-based data service for Lok Sabha data only"""

    def __init__(self):
        self.data_root = Path("app/data")
        self._elections_cache = None
        self._candidates_cache = None
        self._parties_cache = None
        self._constituencies_cache = None
        self._parties_by_id_cache = None
        self._constituencies_by_id_cache = None

    def get_elections(self) -> List[Election]:
        """Get all available elections (only Lok Sabha 2024)"""
        if self._elections_cache is None:
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

    def _load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                print(f"File not found: {file_path}")
                return []
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return []

    def get_candidates(self, election_id: str) -> List[Dict[str, Any]]:
        """Get all candidates for Lok Sabha 2024"""
        if election_id != "lok-sabha-2024":
            return []

        if self._candidates_cache is None:
            file_path = (
                self.data_root / "lok_sabha" / "lok-sabha-2024" / "candidates.json"
            )
            self._candidates_cache = self._load_json_file(file_path)

        return self._candidates_cache

    def get_parties(self, election_id: str) -> List[Party]:
        """Get all parties for Lok Sabha 2024"""
        if election_id != "lok-sabha-2024":
            return []

        if self._parties_cache is None:
            file_path = self.data_root / "lok_sabha" / "lok-sabha-2024" / "parties.json"
            data = self._load_json_file(file_path)
            self._parties_cache = [Party(**party_data) for party_data in data]

        return self._parties_cache

    def get_constituencies(self, election_id: str) -> List[Constituency]:
        """Get all constituencies for Lok Sabha 2024"""
        if election_id != "lok-sabha-2024":
            return []

        if self._constituencies_cache is None:
            file_path = (
                self.data_root / "lok_sabha" / "lok-sabha-2024" / "constituencies.json"
            )
            data = self._load_json_file(file_path)
            self._constituencies_cache = [
                Constituency(**const_data) for const_data in data
            ]

        return self._constituencies_cache

    def _get_parties_by_id(self, election_id: str) -> Dict[str, Party]:
        """Get parties indexed by ID for fast lookup"""
        if self._parties_by_id_cache is None:
            parties = self.get_parties(election_id)
            self._parties_by_id_cache = {party.id: party for party in parties}
        return self._parties_by_id_cache

    def _get_constituencies_by_id(
        self, election_id: str
    ) -> Dict[str, Constituency]:
        """Get constituencies indexed by ID for fast lookup"""
        if self._constituencies_by_id_cache is None:
            constituencies = self.get_constituencies(election_id)
            self._constituencies_by_id_cache = {
                const.id: const for const in constituencies
            }
        return self._constituencies_by_id_cache

    def enrich_candidate_data(
        self, candidate: Dict[str, Any], election_id: str
    ) -> Dict[str, Any]:
        """Enrich candidate data with party and constituency details"""
        enriched = candidate.copy()

        # Add election_id
        enriched["election_id"] = election_id

        # Add party details
        parties_by_id = self._get_parties_by_id(election_id)
        party_id = candidate.get("party_id")
        if party_id and party_id in parties_by_id:
            party = parties_by_id[party_id]
            enriched["party_name"] = party.name
            enriched["party_short_name"] = party.short_name
            enriched["party_symbol"] = party.symbol
        else:
            enriched["party_name"] = "INDEPENDENT" if party_id == "UNKNOWN" else "Unknown"
            enriched["party_short_name"] = "IND" if party_id == "UNKNOWN" else "UNK"
            enriched["party_symbol"] = ""

        # Add constituency details
        constituencies_by_id = self._get_constituencies_by_id(election_id)
        constituency_id = candidate.get("constituency_id")
        if constituency_id and constituency_id in constituencies_by_id:
            constituency = constituencies_by_id[constituency_id]
            enriched["constituency_name"] = constituency.name
            enriched["constituency_state_id"] = constituency.state_id
        else:
            enriched["constituency_name"] = "Unknown"
            enriched["constituency_state_id"] = ""

        return enriched

    def search_candidates(
        self, query: str, election_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search candidates by name, party, or constituency"""
        if election_id and election_id != "lok-sabha-2024":
            return []

        candidates = self.get_candidates("lok-sabha-2024")
        results = []
        query_lower = query.lower()

        for candidate in candidates:
            # Enrich candidate data first
            enriched_candidate = self.enrich_candidate_data(
                candidate, "lok-sabha-2024"
            )

            # Search in multiple fields
            if (
                query_lower in enriched_candidate.get("name", "").lower()
                or query_lower in enriched_candidate.get("party_name", "").lower()
                or query_lower
                in enriched_candidate.get("constituency_name", "").lower()
                or query_lower in enriched_candidate.get("state_name", "").lower()
            ):
                results.append(enriched_candidate)

        return results

    def get_candidate_by_id(
        self, candidate_id: str, election_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific candidate by ID"""
        if election_id != "lok-sabha-2024":
            return None

        candidates = self.get_candidates(election_id)

        for candidate in candidates:
            if candidate.get("id") == candidate_id:
                return self.enrich_candidate_data(candidate, election_id)

        return None

    def get_party_by_name(self, party_name: str, election_id: str) -> Optional[Party]:
        """Get a specific party by name"""
        if election_id != "lok-sabha-2024":
            return None

        parties = self.get_parties(election_id)
        party_name_lower = party_name.lower()

        for party in parties:
            if (
                party.name.lower() == party_name_lower
                or party.short_name.lower() == party_name_lower
            ):
                return party

        return None

    def get_constituency_by_id(
        self, constituency_id: str, election_id: str
    ) -> Optional[Constituency]:
        """Get a specific constituency by ID"""
        if election_id != "lok-sabha-2024":
            return None

        constituencies = self.get_constituencies(election_id)

        for constituency in constituencies:
            if constituency.id == constituency_id:
                return constituency

        return None
