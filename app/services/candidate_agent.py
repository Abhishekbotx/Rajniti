"""
Candidate Data Population Agent

This agent automatically populates detailed candidate information using Perplexity AI.
It finds candidates with missing data, fetches the information, and updates the database.
"""

import json
import logging
import time
import re
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.database.models import Candidate
from app.schemas.candidate_data import (
    EducationDetails,
    PoliticalHistory,
    FamilyMember,
    AssetDetails,
    LiabilityDetails,
    CrimeCaseDetails,
)
from app.services.perplexity_service import PerplexityService

logger = logging.getLogger(__name__)


class CandidateDataAgent:
    """
    Agent for populating candidate detailed information using Perplexity AI.

    This agent:
    1. Finds candidates with missing detailed information
    2. Uses Perplexity AI to fetch the data in a structured format
    3. Updates the database with the fetched information
    """

    def __init__(self, search_service: Optional[Any] = None, perplexity_api_key: Optional[str] = None):
        """
        Initialize the candidate data agent.

        Args:
            search_service: Optional search service instance. If not provided,
                          PerplexityService will be used.
            perplexity_api_key: Optional Perplexity API key.
        """
        self.search_service = search_service or PerplexityService(api_key=perplexity_api_key)
        logger.info("CandidateDataAgent initialized successfully")

    def find_candidates_needing_data(
        self, session: Session, limit: int = 100
    ) -> List[Candidate]:
        """
        Find candidates that are missing detailed information.

        Args:
            session: Database session
            limit: Maximum number of candidates to return

        Returns:
            List of Candidate objects that need data population
        """
        logger.info(f"Finding candidates needing data (limit: {limit})")

        # Query candidates where at least one detailed field is null
        candidates = (
            session.query(Candidate)
            .filter(
                (Candidate.education_background.is_(None))
                | (Candidate.political_background.is_(None))
                | (Candidate.family_background.is_(None))
                | (Candidate.assets.is_(None))
                | (Candidate.liabilities.is_(None))
                | (Candidate.crime_cases.is_(None))
            )
            .limit(limit)
            .all()
        )

        logger.info(f"Found {len(candidates)} candidates needing data")
        return candidates

    def _create_data_query(self, candidate: Candidate, data_type: str) -> str:
        """
        Create a Perplexity query to fetch specific candidate data.

        Args:
            candidate: Candidate object
            data_type: Type of data to fetch (education, political, family, assets, liabilities, crime)

        Returns:
            Formatted query string
        """
        base_info = f"{candidate.name}"

        # Add constituency info if available
        if candidate.constituency_id:
            base_info += f" from constituency {candidate.constituency_id}"

        # We use MyNeta as a reference but do not include source text in the final stored data.
        source_instruction = "Search for this information using reliable sources like MyNeta.info."
        
        common_instruction = (
            f"{source_instruction} "
            "If the information is not available, return an empty list []. "
            "Return ONLY the raw JSON object, no markdown formatting, no code blocks, no other text. "
            "Do not include any source citations, links, or 'According to...' phrases in the values. "
            "Ensure valid JSON format."
        )

        queries = {
            "education": (
                f"What is the education background of Indian politician {base_info}? "
                f"Provide a list of educational qualifications with year, college, stream, and other details. "
                f"{common_instruction} "
                f"Format: [{{'year': '...', 'college': '...', 'stream': '...', 'other_details': '...'}}]"
            ),
            "political": (
                f"What is the political history of Indian politician {base_info}? "
                f"List all elections contested with party, constituency, election_year, position (MP/MLA), and result (WON/LOST). "
                f"{common_instruction} "
                f"Format: [{{'party': '...', 'constituency': '...', 'election_year': '...', 'position': '...', 'result': 'WON/LOST'}}]"
            ),
            "family": (
                f"What is the family background of Indian politician {base_info}? "
                f"Provide information about family members including name, profession, relation, and age. "
                f"{common_instruction} "
                f"Format: [{{'name': '...', 'profession': '...', 'relation': '...', 'age': '...'}}]"
            ),
            "assets": (
                f"What are the declared assets of Indian politician {base_info}? "
                f"List assets with type (CASH/BOND/LAND/EQUITY/AUTOMOBILE/JEWELRY/OTHER), amount, description, and owned_by (SELF/SPOUSE/DEPENDENT/HUF/OTHER). "
                f"{common_instruction} "
                f"Format: [{{'type': '...', 'amount': 1000.0, 'description': '...', 'owned_by': '...'}}]"
            ),
            "liabilities": (
                f"What are the declared liabilities of Indian politician {base_info}? "
                f"List liabilities with type (LOAN/OTHER), amount, description, and owned_by (SELF/SPOUSE/DEPENDENT/HUF/OTHER). "
                f"{common_instruction} "
                f"Format: [{{'type': '...', 'amount': 1000.0, 'description': '...', 'owned_by': '...'}}]"
            ),
            "crime_cases": (
                f"What are the criminal cases against Indian politician {base_info}? "
                f"List cases with FIR No, Police Station, Sections Applied (as list), Charges Framed (boolean), and description. "
                f"{common_instruction} "
                f"Format: [{{'fir_no': '...', 'police_station': '...', 'sections_applied': ['...'], 'charges_framed': true/false, 'description': '...'}}]"
            ),
        }

        return queries.get(data_type, "")

    def _extract_json_from_response(
        self, response_text: str
    ) -> Optional[Any]:
        """
        Extract JSON data from Perplexity response.

        Args:
            response_text: Raw response text from Perplexity

        Returns:
            Parsed JSON object or None if extraction fails
        """
        try:
            # Remove markdown code blocks if present
            match = re.search(r"```(?:json)?\s*(.*?)```", response_text, re.DOTALL)
            if match:
                response_text = match.group(1)
            
            # Strip whitespace
            response_text = response_text.strip()

            # Try to parse directly
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                pass

            # Fallback: find array or object
            # Try to find JSON in the response
            start_idx_list = response_text.find("[")
            end_idx_list = response_text.rfind("]")
            
            start_idx_dict = response_text.find("{")
            end_idx_dict = response_text.rfind("}")

            if start_idx_list != -1 and end_idx_list != -1:
                 # If [ is before {, it's likely a list at root.
                 if start_idx_dict == -1 or start_idx_list < start_idx_dict:
                     json_str = response_text[start_idx_list : end_idx_list + 1]
                     return json.loads(json_str)
            
            if start_idx_dict != -1 and end_idx_dict != -1:
                json_str = response_text[start_idx_dict : end_idx_dict + 1]
                return json.loads(json_str)

            return None
        except Exception as e:
            logger.warning(f"Failed to parse JSON from response: {e}")
            # Log the raw response for debugging
            logger.debug(f"Raw response: {response_text[:200]}...") 
            return None

    def fetch_education_background(
        self, candidate: Candidate
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch education background."""
        logger.info(f"Fetching education background for {candidate.name}")
        try:
            query = self._create_data_query(candidate, "education")
            result = self.search_service.search_india(query)
            
            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))
            if isinstance(data, dict):
                data = [data]

            if isinstance(data, list):
                # Validate with Pydantic
                validated_data = []
                for item in data:
                    try:
                        validated_data.append(EducationDetails(**item).dict())
                    except ValidationError as ve:
                        logger.warning(f"Skipping invalid education data for {candidate.name}: {ve}")
                
                if validated_data:
                    logger.info(f"✅ Education data found for {candidate.name} ({len(validated_data)} records)")
                    return validated_data
            return None
        except Exception as e:
            logger.error(f"Error fetching education background: {e}")
            return None

    def fetch_political_background(
        self, candidate: Candidate
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch political background."""
        logger.info(f"Fetching political background for {candidate.name}")
        try:
            query = self._create_data_query(candidate, "political")
            result = self.search_service.search_india(query)
            
            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))
            if isinstance(data, dict):
                data = [data]

            if isinstance(data, list):
                validated_data = []
                for item in data:
                    try:
                        validated_data.append(PoliticalHistory(**item).dict())
                    except ValidationError as ve:
                         logger.warning(f"Skipping invalid political data for {candidate.name}: {ve}")

                if validated_data:
                    logger.info(f"✅ Political history found for {candidate.name} ({len(validated_data)} records)")
                    return validated_data
            return None
        except Exception as e:
            logger.error(f"Error fetching political background: {e}")
            return None

    def fetch_family_background(
        self, candidate: Candidate
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch family background."""
        logger.info(f"Fetching family background for {candidate.name}")
        try:
            query = self._create_data_query(candidate, "family")
            result = self.search_service.search_india(query)
            
            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))
            if isinstance(data, dict):
                data = [data]

            if isinstance(data, list):
                validated_data = []
                for item in data:
                    try:
                        validated_data.append(FamilyMember(**item).dict())
                    except ValidationError as ve:
                        logger.warning(f"Skipping invalid family data for {candidate.name}: {ve}")

                if validated_data:
                    logger.info(f"✅ Family data found for {candidate.name} ({len(validated_data)} records)")
                    return validated_data
            return None
        except Exception as e:
            logger.error(f"Error fetching family background: {e}")
            return None

    def fetch_assets(
        self, candidate: Candidate
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch assets."""
        logger.info(f"Fetching assets information for {candidate.name}")
        try:
            query = self._create_data_query(candidate, "assets")
            result = self.search_service.search_india(query)
            
            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))
            if isinstance(data, dict):
                data = [data]

            if isinstance(data, list):
                validated_data = []
                for item in data:
                    try:
                        validated_data.append(AssetDetails(**item).dict())
                    except ValidationError as ve:
                         logger.warning(f"Skipping invalid asset data for {candidate.name}: {ve}")

                if validated_data:
                    logger.info(f"✅ Assets information found for {candidate.name} ({len(validated_data)} records)")
                    return validated_data
            return None
        except Exception as e:
            logger.error(f"Error fetching assets: {e}")
            return None

    def fetch_liabilities(
        self, candidate: Candidate
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch liabilities."""
        logger.info(f"Fetching liabilities information for {candidate.name}")
        try:
            query = self._create_data_query(candidate, "liabilities")
            result = self.search_service.search_india(query)
            
            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))
            if isinstance(data, dict):
                data = [data]

            if isinstance(data, list):
                validated_data = []
                for item in data:
                    try:
                        validated_data.append(LiabilityDetails(**item).dict())
                    except ValidationError as ve:
                         logger.warning(f"Skipping invalid liability data for {candidate.name}: {ve}")

                if validated_data:
                    logger.info(f"✅ Liabilities information found for {candidate.name} ({len(validated_data)} records)")
                    return validated_data
            return None
        except Exception as e:
            logger.error(f"Error fetching liabilities: {e}")
            return None

    def fetch_crime_cases(
        self, candidate: Candidate
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch crime cases."""
        logger.info(f"Fetching crime cases for {candidate.name}")
        try:
            query = self._create_data_query(candidate, "crime_cases")
            result = self.search_service.search_india(query)
            
            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))
            if isinstance(data, dict):
                data = [data]

            if isinstance(data, list):
                validated_data = []
                for item in data:
                    try:
                        validated_data.append(CrimeCaseDetails(**item).dict())
                    except ValidationError as ve:
                         logger.warning(f"Skipping invalid crime case data for {candidate.name}: {ve}")

                if validated_data:
                    logger.info(f"✅ Crime cases found for {candidate.name} ({len(validated_data)} records)")
                    return validated_data
            return None
        except Exception as e:
            logger.error(f"Error fetching crime cases: {e}")
            return None

    def populate_candidate_data(
        self,
        session: Session,
        candidate: Candidate,
        delay_between_requests: float = 2.0,
    ) -> Dict[str, bool]:
        """
        Populate all missing data fields for a candidate.

        Args:
            session: Database session
            candidate: Candidate object to populate
            delay_between_requests: Delay in seconds between API requests

        Returns:
            Dictionary with status of each field update
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing candidate: {candidate.name} (ID: {candidate.id})")
        logger.info(f"{'='*60}\n")

        status = {
            "education": False,
            "political": False,
            "family": False,
            "assets": False,
            "liabilities": False,
            "crime_cases": False,
        }

        update_data = {}

        # Helper to fetch and update
        def fetch_and_update(field_name, fetch_method, status_key):
            if getattr(candidate, field_name) is None:
                data = fetch_method(candidate)
                # Strict validation: reject empty lists if not explicit
                if data is not None:
                    update_data[field_name] = data
                    status[status_key] = True
                time.sleep(delay_between_requests)
            else:
                logger.info(f"⏭️  {status_key.capitalize()} data already exists for {candidate.name}")
                status[status_key] = True

        fetch_and_update("education_background", self.fetch_education_background, "education")
        fetch_and_update("political_background", self.fetch_political_background, "political")
        fetch_and_update("family_background", self.fetch_family_background, "family")
        fetch_and_update("assets", self.fetch_assets, "assets")
        fetch_and_update("liabilities", self.fetch_liabilities, "liabilities")
        fetch_and_update("crime_cases", self.fetch_crime_cases, "crime_cases")

        # Update candidate if we have new data
        if update_data:
            try:
                candidate.update(session, **update_data)
                session.commit()
                logger.info(
                    f"✅ Successfully updated {candidate.name} with {len(update_data)} fields"
                )
            except Exception as e:
                session.rollback()
                logger.error(f"❌ Failed to update candidate: {e}")

        logger.info(f"\n📋 Summary for {candidate.name}:")
        for key, val in status.items():
            logger.info(f"   - {key.capitalize()}: {'✓' if val else '✗'}")

        return status

    def run(
        self,
        session: Session,
        batch_size: int = 10,
        delay_between_candidates: float = 2.0,
        delay_between_requests: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Run the agent to populate data for multiple candidates.

        Args:
            session: Database session
            batch_size: Number of candidates to process in one run
            delay_between_candidates: Delay in seconds between processing candidates
            delay_between_requests: Delay in seconds between API requests for same candidate

        Returns:
            Summary statistics of the run
        """
        logger.info("\n" + "=" * 60)
        logger.info("🚀 Starting Candidate Data Population Agent")
        logger.info("=" * 60 + "\n")
        logger.info(f"Batch size: {batch_size}")
        logger.info(f"Delay between candidates: {delay_between_candidates}s")
        logger.info(f"Delay between requests: {delay_between_requests}s\n")

        # Find candidates needing data
        candidates = self.find_candidates_needing_data(session, limit=batch_size)

        if not candidates:
            logger.info("✅ No candidates found needing data population")
            return {"total_processed": 0, "successful": 0, "partial": 0, "failed": 0}

        # Process each candidate
        stats = {
            "total_processed": 0,
            "successful": 0,  # All 6 fields populated
            "partial": 0,  # Some fields populated
            "failed": 0,  # No fields populated
        }

        for idx, candidate in enumerate(candidates, 1):
            logger.info(f"\nProcessing {idx}/{len(candidates)}")

            status = self.populate_candidate_data(
                session, candidate, delay_between_requests=delay_between_requests
            )

            stats["total_processed"] += 1

            fields_populated = sum(status.values())
            if fields_populated == 6:
                stats["successful"] += 1
            elif fields_populated > 0:
                stats["partial"] += 1
            else:
                stats["failed"] += 1

            # Delay before next candidate
            if idx < len(candidates):
                time.sleep(delay_between_candidates)

        # Print final summary
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Agent Run Complete")
        logger.info("=" * 60 + "\n")
        logger.info(f"Total candidates processed: {stats['total_processed']}")
        logger.info(f"Fully populated (6/6 fields): {stats['successful']}")
        logger.info(f"Partially populated: {stats['partial']}")
        logger.info(f"Failed to populate: {stats['failed']}")
        logger.info("")

        return stats
