"""
Lok Sabha Election Data Scraper

Single scraper that extracts all election data (parties, constituencies, candidates, metadata)
from ECI Lok Sabha results page.
"""

import logging
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List

from bs4 import BeautifulSoup

from .base import get_with_retry, normalize_base_url, save_json

logger = logging.getLogger(__name__)


class LokSabhaScraper:
    """Scraper for Lok Sabha election data."""

    def __init__(self, url: str):
        """
        Initialize Lok Sabha scraper.

        Args:
            url: ECI Lok Sabha results page URL
                 (e.g., https://results.eci.gov.in/PcResultGenJune2024/index.htm)
        """
        self.base_url = normalize_base_url(url)
        self.year = None
        self.election_name = None
        self.folder_name = None

        # Data storage
        self.parties_data = []
        self.constituencies_data = []
        self.candidates_data = []
        self.metadata = {}

    def _generate_uuid(self) -> str:
        """Generate a unique UUID for a candidate."""
        return str(uuid.uuid4())

    def _generate_party_page_link(self, party_id: str) -> str:
        """Generate a constituency page link from party id."""
        return f"{self.base_url}/partywisewinresultState-{party_id}.htm"

    def _generate_constituency_page_link(
        self, state_id: str, constituency_id: str
    ) -> str:
        """Generate a constituency page link from state and constituency code."""
        return f"{self.base_url}/candidateswise-{state_id}{constituency_id}.htm"

    def scrape(self) -> None:
        """Main scraping orchestrator - scrapes all data and saves to JSON files."""
        logger.info(f"Starting Lok Sabha scraping from {self.base_url}")

        # Extract year and metadata first
        self._extract_metadata()

        # Scrape all data
        # Layer 1: Party-wise results
        logger.info("Scraping party-wise results...")
        parties_data = self._scrape_parties()
        self.parties_data = parties_data

        # Layer 2: Constituencies
        logger.info("Discovering constituencies...")
        constituencies_data = self._scrape_constituencies(parties_data)
        self.constituencies_data = constituencies_data

        # Layer 3: Scrape candidates
        logger.info("Scraping candidates...")
        candidates_data = self._scrape_candidates(constituencies_data)
        self.candidates_data = candidates_data

        # Save all data
        self._save_all_data()

        logger.info("Lok Sabha scraping completed successfully!")
        logger.info(f"  - Parties: {len(self.parties_data)}")
        logger.info(f"  - Constituencies: {len(self.constituencies_data)}")
        logger.info(f"  - Candidates: {len(self.candidates_data)}")

    def _extract_metadata(self) -> None:
        """Extract election metadata from the main page."""
        logger.info("Extracting election metadata...")

        # Try to extract year from URL as primary method
        year_match = re.search(r"20\d{2}", self.base_url)
        self.year = int(year_match.group(0)) if year_match else 2024

        self.election_name = f"Lok Sabha General Election {self.year}"
        self.folder_name = f"lok-sabha-{self.year}"

        logger.info(f"Detected: {self.election_name}")
        logger.info(f"Output folder: {self.folder_name}")

    def _scrape_parties(self) -> None:
        """Scrape party-wise results and compile party list with seat counts."""
        parties_data = self._discover_parties_details()

        if not parties_data:
            logger.warning("No parties discovered")
            return

        logger.info(f"Found {len(parties_data)} parties, scraping results...")

        return parties_data

    def _discover_parties_details(self) -> List[Dict[str, str]]:
        """Discover party links from main results page."""
        parties_data = []

        urls_to_try = [
            f"{self.base_url}/index.htm",
        ]

        for url in urls_to_try:
            response = get_with_retry(url, referer=self.base_url)
            if not response:
                continue

            soup = BeautifulSoup(response.content, "html.parser")

            # Find the party results table
            table = soup.find("table", {"class": "table"})
            if not table:
                logger.warning("No party table found on main page")
                return parties_data

            tbody = table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        full_name = cols[0].text.strip()
                        name = full_name.split(" - ")[0]
                        short_name = full_name.split(" - ")[1]
                        id = cols[1].find("a")["href"].split("-")[-1].split(".")[0]
                        parties_data.append(
                            {
                                "id": id,
                                "name": name,
                                "short_name": short_name,
                                "symbol": "",
                            }
                        )

        return parties_data

    def _scrape_constituencies(self, parties_data: List[Dict[str, Any]]) -> None:
        """Discover and scrape constituency data."""
        constituencies_data = self._discover_constituency_details(parties_data)

        return constituencies_data

    def _discover_constituency_details(
        self, parties_data: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Auto-discover constituency details from main page."""
        logger.info("Discovering constituency details...")
        constituencies_data = []
        seen_constituencies = set()  # Track unique constituencies to avoid duplicates

        # Fetch Constituency Results page
        for party in parties_data:
            party_id = party["id"]
            party_name = party["name"]

            url = self._generate_party_page_link(party_id)
            response = get_with_retry(url, referer=self.base_url)
            if not response:
                logger.warning(f"Could not fetch party results page for {party_name}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", {"class": "table"})
            if not table:
                logger.warning(f"No party table found on {party_name} results page")
                continue

            tbody = table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 1:
                        a_tag = cols[1].find("a")
                        consituency_name = (
                            a_tag.text.strip().split("(")[0]
                            if a_tag
                            else cols[1].text.strip().split("(")[0]
                        )
                        link = (
                            a_tag["href"] if a_tag and a_tag.has_attr("href") else None
                        )

                        if link:
                            state_constituency_id = link.split("-")[-1].split(".")[0]
                            state_id = state_constituency_id[:3]
                            constituency_id = state_constituency_id[3:]

                            # Use full state+constituency code as unique key
                            unique_key = f"{state_id}{constituency_id}"

                            if unique_key not in seen_constituencies:
                                seen_constituencies.add(unique_key)
                                constituencies_data.append(
                                    {
                                        "id": constituency_id,
                                        "name": consituency_name,
                                        "state_id": state_id,
                                    }
                                )

        logger.info(f"Discovered {len(constituencies_data)} unique constituencies")
        return constituencies_data

    def _scrape_candidates(
        self, constituencies_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Scrape candidate data from constituency pages."""
        candidates_data = self._discover_candidate_details(constituencies_data)

        return candidates_data

    def _discover_candidate_details(
        self, constituencies_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Discover candidate details from constituency pages."""
        candidates_data = []

        for constituency in constituencies_data:
            constituency_id = constituency["id"]
            constituency_name = constituency["name"]
            state_id = constituency["state_id"]

            url = self._generate_constituency_page_link(state_id, constituency_id)
            response = get_with_retry(url, referer=self.base_url)
            if not response:
                logger.warning(
                    f"Could not fetch constituency page for {constituency_name}"
                )
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", {"class": "table"})
            if not table:
                logger.warning(
                    f"No constituency table found on {constituency_name} page"
                )
                continue

            tbody = table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 7:  # Ensure we have enough columns
                        a_tag = cols[1].find("a")
                        candidate_name = (
                            a_tag.text.strip() if a_tag else cols[1].text.strip()
                        )
                        candidate_party_id = cols[2].text.strip()
                        candidate_status = cols[3].text.strip()
                        candidate_image = (
                            cols[6].find("img")["src"] if cols[6].find("img") else None
                        )
                        candidates_data.append(
                            {
                                "id": self._generate_uuid(),
                                "name": candidate_name,
                                "party_id": candidate_party_id,
                                "constituency_id": constituency_id,
                                "state_id": state_id,
                                "status": candidate_status,
                                "type": "MP",
                                "image_url": candidate_image,
                            }
                        )

        logger.info(f"Scraped {len(candidates_data)} candidates")
        return candidates_data

    def _save_all_data(self) -> None:
        """Save all scraped data to JSON files in proper folder structure."""
        base_path = Path("app/data")

        # Create folder paths
        lok_sabha_dir = base_path / "lok_sabha" / self.folder_name
        elections_dir = base_path / "elections"

        # Save parties
        save_json(self.parties_data, lok_sabha_dir / "parties.json")

        # Save constituencies
        save_json(self.constituencies_data, lok_sabha_dir / "constituencies.json")

        # Save candidates
        save_json(self.candidates_data, lok_sabha_dir / "candidates.json")

        # Build and save election metadata
        # Find winning party (party with most seats/wins)
        winning_party = None
        winning_party_seats = 0

        if self.parties_data:
            # Count seats for each party from parties data
            winning_party = self.parties_data[0]["name"]
            # We can't get seat count from current structure, so we'll calculate from candidates
            party_seats = {}
            for candidate in self.candidates_data:
                if candidate.get("status") == "WON":
                    party_id = candidate.get("party_id", "")
                    party_seats[party_id] = party_seats.get(party_id, 0) + 1

            if party_seats:
                winning_party_id = max(party_seats, key=party_seats.get)
                winning_party_seats = party_seats[winning_party_id]
                # Find the party name from party_id
                for party in self.parties_data:
                    if party["id"] == winning_party_id:
                        winning_party = party["name"]
                        break

        self.metadata = {
            "election_id": self.folder_name,
            "name": self.election_name,
            "type": "LOK_SABHA",
            "year": self.year,
            "date": None,
            "total_constituencies": len(self.constituencies_data),
            "total_candidates": len(self.candidates_data),
            "total_parties": len(self.parties_data),
            "result_status": "DECLARED",
            "winning_party": winning_party,
            "winning_party_seats": winning_party_seats,
        }

        save_json([self.metadata], elections_dir / f"LS-{self.year}.json")

        logger.info(f"All data saved successfully to {lok_sabha_dir}")
