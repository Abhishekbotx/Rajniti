"""
Lok Sabha Election Data Scraper

Single scraper that extracts all election data (parties, constituencies, candidates, metadata)
from ECI Lok Sabha results page.
"""

import logging
import re
import time
import uuid
from pathlib import Path
from typing import Dict, List

from bs4 import BeautifulSoup

from .base import (
    clean_margin,
    clean_votes,
    get_with_retry,
    normalize_base_url,
    save_json,
)

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
        self.all_states=[]

    def _generate_uuid(self) -> str:
        """Generate a unique UUID for a candidate."""
        return str(uuid.uuid4())

    def scrape(self) -> None:
        """Main scraping orchestrator - scrapes all data and saves to JSON files."""
        logger.info(f"Starting Lok Sabha scraping from {self.base_url}")

        # Extract year and metadata first
        self._extract_metadata()

        # Scrape all data
        # Layer 1: Party-wise results
        logger.info("Scraping party-wise results...")
        self._scrape_parties()

        # Layer 2: Constituencies
        logger.info("Discovering constituencies...")
        self._scrape_constituencies()

        # Layer 3: Candidates
        logger.info("Candidates already scraped from party pages")

        # Save all data
        self._save_all_data()

        logger.info(f"Lok Sabha scraping completed successfully!")
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
        # Discover party links from main page
        party_details = self._discover_parties_details()
        print("HERE", party_details)

        if not party_details:
            logger.warning("No parties discovered")
            return

        # Track candidates by party to count seats
        party_candidates = {}

        logger.info(f"Found {len(party_details)} parties, scraping results...")

        for idx, party_info in enumerate(party_details, 1):
            party_id = party_info["party_id"]
            party_name = party_info.get("name", f"Party {party_id}")

            logger.info(f"  [{idx}/{len(party_details)}] {party_name}")

            # Try party-wise winning results page
            url = f"{self.base_url}/partywisewinresultState-{party_id}.htm"
            response = get_with_retry(url, referer=self.base_url)

            if not response:
                # Try alternative URL pattern
                url = f"{self.base_url}/partywisewinresultState-{party_id}.htm"
                response = get_with_retry(url, referer=self.base_url)

            if response:
                soup = BeautifulSoup(response.content, "html.parser")
                table = soup.find("table", {"class": "table"})

                if table:
                    tbody = table.find("tbody")
                    if tbody:
                        rows = tbody.find_all("tr")
                        for row in rows:
                            cols = row.find_all("td")
                            if len(cols) >= 3:
                                candidate_name = (
                                    cols[2].text.strip() if len(cols) > 2 else ""
                                )
                                constituency = (
                                    cols[1].text.strip() if len(cols) > 1 else ""
                                )
                                state_constituency_id=(
                                    cols[1].find("a")["href"].split("-")[-1].split(".")[0]
                                )
                                votes = cols[3].text.strip() if len(cols) > 3 else ""
                                margin = cols[4].text.strip() if len(cols) > 4 else ""

                                # Store for candidates data
                                if party_id not in party_candidates:
                                    party_candidates[party_id] = []
                                
                                party_candidates[party_id].append({
                                    "uuid": self._generate_uuid(),
                                    "party_id": int(party_id),
                                    "constituency": constituency,
                                    "candidate_name": candidate_name,
                                    "votes": votes,
                                    "margin": margin,
                                    "state_constituency_id":state_constituency_id
                                })
            
            time.sleep(0.3)  # Be polite to server

        # Build parties list with seat counts
        for party_info in party_details:
            party_id = party_info["party_id"]
            party_name = party_info["name"]

            # Parse party name and symbol
            if " - " in party_name:
                name_part, symbol_part = party_name.split(" - ", 1)
            else:
                name_part = party_name
                symbol_part = ""

            # Count seats (candidates that won from this party)
            seat_count = len(party_candidates.get(party_id, []))

            self.parties_data.append(
                {
                    "party_name": name_part.strip(),
                    "symbol": symbol_part.strip(),
                    "total_seats": seat_count,
                }
            )

        # Store all candidates from party pages
        for party_id, candidates in party_candidates.items():
            self.candidates_data.extend(candidates)

        # Sort parties by seats won (descending)
        self.parties_data.sort(key=lambda x: (-x["total_seats"], x["party_name"]))

        logger.info(f"Scraped {len(self.parties_data)} parties")

    def _discover_parties_details(self) -> List[Dict[str, str]]:
        """Discover party links from main results page."""
        party_details = []

        # Try multiple pages
        urls_to_try = [
            f"{self.base_url}/index.htm",
        ]

        for url in urls_to_try:
            response = get_with_retry(url, referer=self.base_url)
            if not response:
                continue

            # print("response here ::", response.content)
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the party results table
            table = soup.find("table", {"class": "table"})
            if not table:
                logger.warning("No party table found on main page")
                return party_details

            tbody = table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        party_full_name = cols[0].text.strip()
                        party_name = party_full_name.split(" - ")[0]
                        party_short_name = party_full_name.split(" - ")[1]
                        seats_won = cols[1].text.strip()
                        party_id = cols[1].find("a")["href"].split("-")[-1].split(".")[0]
                        party_details.append({
                            "name": party_name,
                            "short_name": party_short_name,
                            "seats_won": seats_won,
                            "party_id": party_id
                        })

        # Remove duplicates
        seen = set()
        unique_parties = []
        for party in party_details:
            if party["party_id"] not in seen:
                seen.add(party["party_id"])
                unique_parties.append(party)

        return unique_parties

    def _scrape_constituencies(self) -> None:
        """Discover and scrape constituency data."""
        constituency_links = self._discover_constituency_links()
        states_and_ut=self._discover_states_and_ut()
        
        self.all_states.append(states_and_ut)
        
        # allconstituencies=[]
        for state in states_and_ut:
            print("state he in all statesut:",state)
            res=self._discover_constituencies_by_state(state["state_code"],state["name"])
            print("state he in all statesut res:",res)
            
            for constituencies in res:
                const_id = constituencies["constituency_code"]
                const_name = constituencies["name"]
                const_constituencynumber = constituencies["constituency_number"]
                const_state_id=state["state_code"]
    
                self.constituencies_data.append(
                    {
                        "constituency_id": const_id,
                        "constituency_name": const_name,
                        "constituency_number": const_constituencynumber,
                        "state_id": const_state_id,  # Lok Sabha
                    }
                )
        

        # for const in constituency_links:
        #     # Extract constituency ID from code
        #     const_id = const["constituency_code"]
        #     const_name = const.get("name", "")

        #     self.constituencies_data.append(
        #         {
        #             "constituency_id": const_id,
        #             "constituency_name": const_name,
        #             "state_id": "LS",  # Lok Sabha
        #         }
        #     )

        logger.info(f"Found {len(self.constituencies_data)} constituencies")

    
    #Extracting constituencies Logic 
    def _discover_states_and_ut(self) -> List[Dict[str, str]]:
        """scape states and ut code from main page."""
        logger.info("Discovering states and union territories...")
        states=[]
        
        url = f"{self.base_url}/index.htm"
        response=get_with_retry(url,referer=self.base_url)
        
        if not response:
            logger.warning("couldnt'fetch states/UTs from index page")
            return states
        
        soup=BeautifulSoup(response.content,"html.parser")
        select_tag = soup.find("select", {"name": "state"})
        
        if not select_tag:
            logger.error("State/UT dropdown not found on the main page!")
            return select_tag
        
        # Extract state and UT codes in options tag
        for option in select_tag.find_all("option"):
            value = option.get("value")
            if value:
                code=option.get("value")
                name=option.get_text(strip=True)
                states.append({
                    "state_code":code,
                    "name":name
                })

        # Remove duplicates
        seen = set()
        unique_states = []
        for const in states:
            if const["state_code"] not in seen:
                seen.add(const["state_code"])
                unique_states.append(const)

        logger.info(f"Discovered {len(unique_states)} states and UTs")
        return unique_states                
    
    def _discover_constituencies_by_state(self,state_code: str,state_name: str) -> List[Dict[str, str]]:
        """scape states and ut code from main page."""
        logger.info(f"Discovering constituencies for {state_name}...")
        constituencies=[]
        
        url = f"{self.base_url}/partywiseresult-{state_code}.htm"
        response=get_with_retry(url,referer=self.base_url)
        
        if not response:
            logger.warning(f"couldnt'fetch constuencies for {state_name}")
            return constituencies
        
        soup=BeautifulSoup(response.content,"html.parser")
        
        
        # Look for states and UT options inside select[name="state"]
        select_tag = soup.find("select", {"name": "state"})
        if not select_tag:
            logger.error(f"Constituency dropdown not found for {state_name}")
            return constituencies
        
        #Look for states and ut code
        for option in select_tag.find_all("option"):
            value=option.get("value")
            if value:
                # Example format: "ConstituencyName - 01"
                val=option.get_text(strip=True).split("-")
                name=option.get_text(strip=True)
                name=val[0]
                constituencies.append({
                    "constituency_code":value,
                    "name":name,
                    "constituency_number":val[1].strip()
                })
                
        # Remove duplicates       
        seen = set()
        unique_constituencies = []
        for const in constituencies:
            if const["constituency_code"] not in seen:
                seen.add(const["constituency_code"])
                unique_constituencies.append(const)

        logger.info(f"Discovered {len(unique_constituencies)} constituencies in {state_name}")
        return unique_constituencies     
    
    def _discover_constituency_links(self) -> List[Dict[str, str]]:
        """Auto-discover constituency links from main page."""
        logger.info("Discovering constituency links...")
        constituency_links = []

        url = f"{self.base_url}/index.htm"
        response = get_with_retry(url, referer=self.base_url)

        if not response:
            logger.warning("Could not fetch index page")
            return constituency_links

        soup = BeautifulSoup(response.content, "html.parser")

        # Look for constituency links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "candidateswise" in href.lower():
                # Extract constituency code
                match = re.search(r"candidateswise-([^.]+)\.htm", href, re.IGNORECASE)
                if match:
                    const_code = match.group(1)
                    const_name = link.get_text(strip=True)
                    constituency_links.append(
                        {
                            "constituency_code": const_code,
                            "name": const_name,
                            "url": (
                                f"{self.base_url}/{href}"
                                if not href.startswith("http")
                                else href
                            ),
                        }
                    )

        # Remove duplicates
        seen = set()
        unique_constituencies = []
        for const in constituency_links:
            if const["constituency_code"] not in seen:
                seen.add(const["constituency_code"])
                unique_constituencies.append(const)

        logger.info(f"Discovered {len(unique_constituencies)} constituencies")
        return unique_constituencies

    def _save_all_data(self) -> None:
        """Save all scraped data to JSON files in proper folder structure."""
        base_path = Path("app/data")

        # Create folder paths
        lok_sabha_dir = base_path / "lok_sabha" / self.folder_name
        elections_dir = base_path / "elections"
        main_dir=base_path / "main"
        
        #Save states
        save_json(self.all_states, main_dir / "states.json")

        # Save parties
        save_json(self.parties_data, lok_sabha_dir / "parties.json")

        # Save constituencies
        save_json(self.constituencies_data, lok_sabha_dir / "constituencies.json")

        # Save candidates
        save_json(self.candidates_data, lok_sabha_dir / "candidates.json")

        # Build and save election metadata
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
            "winning_party": (
                self.parties_data[0]["party_name"] if self.parties_data else None
            ),
            "winning_party_seats": (
                self.parties_data[0]["total_seats"] if self.parties_data else 0
            ),
        }

        save_json([self.metadata], elections_dir / f"LS-{self.year}.json")

        logger.info(f"All data saved successfully to {lok_sabha_dir}")
