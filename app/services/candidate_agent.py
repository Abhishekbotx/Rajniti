"""
Candidate Data Population Agent

This agent automatically populates detailed candidate information using Perplexity AI.
It finds candidates with missing data, fetches the information, and updates the database.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.database.models import Candidate
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

    def __init__(self, perplexity_api_key: Optional[str] = None):
        """
        Initialize the candidate data agent.

        Args:
            perplexity_api_key: Optional Perplexity API key. If not provided,
                              will be read from environment variable.
        """
        self.perplexity = PerplexityService(api_key=perplexity_api_key)
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
            data_type: Type of data to fetch (education, political, family, assets)

        Returns:
            Formatted query string
        """
        base_info = f"{candidate.name}"

        # Add constituency info if available
        if candidate.constituency_id:
            base_info += f" from constituency {candidate.constituency_id}"

        queries = {
            "education": f"What is the education background of Indian politician {base_info}? "
            f"Provide graduation year, stream/field of study, and college/school name in JSON format: "
            f'{{"graduation_year": <year>, "stream": "<field>", "college_or_school": "<name>"}}',
            "political": f"What is the political history of Indian politician {base_info}? "
            f"List all elections contested with year, type (MP/MLA), constituency, party, and result in JSON format: "
            f'{{"elections": [{{"election_year": <year>, "election_type": "<MP/MLA>", '
            f'"constituency": "<name>", "party": "<party>", "status": "<WON/LOST>"}}]}}',
            "family": f"What is the family background of Indian politician {base_info}? "
            f"Provide information about father, mother, spouse, and children with their names and professions in JSON format: "
            f'{{"father": {{"name": "<name>", "profession": "<profession>"}}, '
            f'"mother": {{"name": "<name>", "profession": "<profession>"}}, '
            f'"spouse": {{"name": "<name>", "profession": "<profession>"}}, '
            f'"children": [{{"name": "<name>", "profession": "<profession>"}}]}}',
            "assets": f"What are the declared assets of Indian politician {base_info}? "
            f"Provide commercial assets, cash assets, and bank details in JSON format: "
            f'{{"commercial_assets": "<description>", "cash_assets": "<description>", '
            f'"bank_details": [{{"bank_name": "<name>", "branch": "<branch>"}}]}}',
        }

        return queries.get(data_type, "")

    def _extract_json_from_response(
        self, response_text: str
    ) -> Optional[Dict[str, Any]]:
        """
        Extract JSON data from Perplexity response.

        Args:
            response_text: Raw response text from Perplexity

        Returns:
            Parsed JSON dictionary or None if extraction fails
        """
        try:
            # Try to find JSON in the response
            # Look for content between curly braces
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}")

            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx : end_idx + 1]
                return json.loads(json_str)

            return None
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON from response: {e}")
            return None

    def fetch_education_background(
        self, candidate: Candidate
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch education background for a candidate.

        Args:
            candidate: Candidate object

        Returns:
            Education background dictionary or None if fetch fails
        """
        logger.info(f"Fetching education background for {candidate.name}")

        try:
            query = self._create_data_query(candidate, "education")
            result = self.perplexity.search_india(query)

            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            # Extract JSON from response
            data = self._extract_json_from_response(result.get("answer", ""))

            if data:
                logger.info(f"✅ Education data found for {candidate.name}")
                return data
            else:
                logger.warning(
                    f"⚠️  No structured education data found for {candidate.name}"
                )
                return None

        except Exception as e:
            logger.error(f"Error fetching education background: {e}")
            return None

    def fetch_political_background(
        self, candidate: Candidate
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch political background for a candidate.

        Args:
            candidate: Candidate object

        Returns:
            Political background dictionary or None if fetch fails
        """
        logger.info(f"Fetching political background for {candidate.name}")

        try:
            query = self._create_data_query(candidate, "political")
            result = self.perplexity.search_india(query)

            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))

            if data and "elections" in data:
                logger.info(f"✅ Political history found for {candidate.name}")
                return data
            else:
                logger.warning(
                    f"⚠️  No structured political data found for {candidate.name}"
                )
                return None

        except Exception as e:
            logger.error(f"Error fetching political background: {e}")
            return None

    def fetch_family_background(self, candidate: Candidate) -> Optional[Dict[str, Any]]:
        """
        Fetch family background for a candidate.

        Args:
            candidate: Candidate object

        Returns:
            Family background dictionary or None if fetch fails
        """
        logger.info(f"Fetching family background for {candidate.name}")

        try:
            query = self._create_data_query(candidate, "family")
            result = self.perplexity.search_india(query)

            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))

            if data:
                logger.info(f"✅ Family data found for {candidate.name}")
                return data
            else:
                logger.warning(
                    f"⚠️  No structured family data found for {candidate.name}"
                )
                return None

        except Exception as e:
            logger.error(f"Error fetching family background: {e}")
            return None

    def fetch_assets(self, candidate: Candidate) -> Optional[Dict[str, Any]]:
        """
        Fetch assets information for a candidate.

        Args:
            candidate: Candidate object

        Returns:
            Assets dictionary or None if fetch fails
        """
        logger.info(f"Fetching assets information for {candidate.name}")

        try:
            query = self._create_data_query(candidate, "assets")
            result = self.perplexity.search_india(query)

            if result.get("error"):
                logger.error(f"Perplexity error: {result['error']}")
                return None

            data = self._extract_json_from_response(result.get("answer", ""))

            if data:
                logger.info(f"✅ Assets information found for {candidate.name}")
                return data
            else:
                logger.warning(
                    f"⚠️  No structured assets data found for {candidate.name}"
                )
                return None

        except Exception as e:
            logger.error(f"Error fetching assets: {e}")
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
        }

        update_data = {}

        # Fetch education background if missing
        if candidate.education_background is None:
            education = self.fetch_education_background(candidate)
            if education:
                update_data["education_background"] = education
                status["education"] = True
            time.sleep(delay_between_requests)
        else:
            logger.info(f"⏭️  Education data already exists for {candidate.name}")
            status["education"] = True

        # Fetch political background if missing
        if candidate.political_background is None:
            political = self.fetch_political_background(candidate)
            if political:
                update_data["political_background"] = political
                status["political"] = True
            time.sleep(delay_between_requests)
        else:
            logger.info(f"⏭️  Political data already exists for {candidate.name}")
            status["political"] = True

        # Fetch family background if missing
        if candidate.family_background is None:
            family = self.fetch_family_background(candidate)
            if family:
                update_data["family_background"] = family
                status["family"] = True
            time.sleep(delay_between_requests)
        else:
            logger.info(f"⏭️  Family data already exists for {candidate.name}")
            status["family"] = True

        # Fetch assets if missing
        if candidate.assets is None:
            assets = self.fetch_assets(candidate)
            if assets:
                update_data["assets"] = assets
                status["assets"] = True
            time.sleep(delay_between_requests)
        else:
            logger.info(f"⏭️  Assets data already exists for {candidate.name}")
            status["assets"] = True

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
        logger.info(f"   - Education: {'✓' if status['education'] else '✗'}")
        logger.info(f"   - Political History: {'✓' if status['political'] else '✗'}")
        logger.info(f"   - Family: {'✓' if status['family'] else '✗'}")
        logger.info(f"   - Assets: {'✓' if status['assets'] else '✗'}")

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
            "successful": 0,  # All 4 fields populated
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
            if fields_populated == 4:
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
        logger.info(f"Fully populated (4/4 fields): {stats['successful']}")
        logger.info(f"Partially populated: {stats['partial']}")
        logger.info(f"Failed to populate: {stats['failed']}")
        logger.info("")

        return stats
