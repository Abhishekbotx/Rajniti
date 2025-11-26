"""
Optimized Candidate Data Population Agent

This is an optimized version of the candidate agent that:
1. Uses batch queries to combine multiple API calls into one
2. Implements caching to avoid redundant calls
3. Supports multiple LLM providers (Perplexity, OpenAI, Anthropic)
4. Only fetches missing data fields
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
from app.services.llm_service import get_llm_service
from app.services.llm_cache import get_cache
from app.services.vector_db_pipeline import VectorDBPipeline

logger = logging.getLogger(__name__)


class CandidateAgent:
    """
    Optimized agent for populating candidate detailed information.

    Key optimizations:
    - Batch queries: Combines multiple data requests into single API call
    - Caching: Avoids redundant API calls for similar queries
    - Multi-provider support: Can use Perplexity, OpenAI, or Anthropic
    - Smart fetching: Only fetches missing fields
    """

    def __init__(
        self,
        llm_provider: Optional[str] = None,
        enable_cache: bool = True,
        cache_ttl_hours: int = 24,
        enable_vector_db: bool = True,
    ):
        """
        Initialize the optimized candidate data agent.

        Args:
            llm_provider: LLM provider name ('perplexity', 'openai', 'anthropic').
                         If None, reads from LLM_PROVIDER env var
            enable_cache: Whether to enable response caching
            cache_ttl_hours: Cache TTL in hours
            enable_vector_db: Whether to automatically sync to vector DB
        """
        # Initialize LLM service
        self.search_service = get_llm_service(provider=llm_provider)
        logger.info(f"Using LLM provider: {llm_provider or 'default'}")

        # Initialize cache
        self.cache = get_cache(ttl_hours=cache_ttl_hours) if enable_cache else None
        if enable_cache:
            logger.info(f"Response caching enabled (TTL: {cache_ttl_hours} hours)")

        self.enable_vector_db = enable_vector_db
        self.vector_db_pipeline = None

        if enable_vector_db:
            try:
                self.vector_db_pipeline = VectorDBPipeline()
                logger.info("Vector DB pipeline initialized for automatic sync")
            except Exception as e:
                logger.warning(f"Failed to initialize vector DB pipeline: {e}")
                logger.warning("Continuing without vector DB sync")
                self.enable_vector_db = False

        logger.info("CandidateAgent initialized successfully")

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
        from sqlalchemy import or_, cast, Text

        logger.info(f"Finding candidates needing data (limit: {limit})")

        def is_null_or_empty(field):
            """Check if a JSON field is NULL or an empty array/object"""
            return or_(
                field.is_(None),
                cast(field, Text) == "[]",
                cast(field, Text) == "{}",
                cast(field, Text) == "null",
            )

        candidates = (
            session.query(Candidate)
            .filter(
                or_(
                    is_null_or_empty(Candidate.education_background),
                    is_null_or_empty(Candidate.political_background),
                    is_null_or_empty(Candidate.family_background),
                    is_null_or_empty(Candidate.assets),
                    is_null_or_empty(Candidate.liabilities),
                    is_null_or_empty(Candidate.crime_cases),
                )
            )
            .limit(limit)
            .all()
        )

        logger.info(f"Found {len(candidates)} candidates needing data")
        return candidates

    def _create_batch_query(
        self, candidate: Candidate, data_types: List[str]
    ) -> str:
        """
        Create a single batch query for multiple data types.

        This is the KEY OPTIMIZATION: Instead of 6 separate API calls,
        we combine them into one.

        Args:
            candidate: Candidate object
            data_types: List of data types to fetch (e.g., ['education', 'political'])

        Returns:
            Combined query string
        """
        base_info = f"{candidate.name}"
        if candidate.constituency_id:
            base_info += f" from constituency {candidate.constituency_id}"

        query_parts = []
        formats = {
            "education": "[{'year': '...', 'college': '...', 'stream': '...', 'other_details': '...'}]",
            "political": "[{'party': '...', 'constituency': '...', 'election_year': '...', 'position': '...', 'result': 'WON/LOST'}]",
            "family": "[{'name': '...', 'profession': '...', 'relation': '...', 'age': '...'}]",
            "assets": "[{'type': '...', 'amount': 1000.0, 'description': '...', 'owned_by': '...'}]",
            "liabilities": "[{'type': '...', 'amount': 1000.0, 'description': '...', 'owned_by': '...'}]",
            "crime_cases": "[{'fir_no': '...', 'police_station': '...', 'sections_applied': ['...'], 'charges_framed': true/false, 'description': '...'}]",
        }

        descriptions = {
            "education": "education background with year, college, stream, and other details",
            "political": "political history with all elections contested (party, constituency, election_year, position, result)",
            "family": "family background with family members (name, profession, relation, age)",
            "assets": "declared assets (type: CASH/BOND/LAND/EQUITY/AUTOMOBILE/JEWELRY/OTHER, amount, description, owned_by)",
            "liabilities": "declared liabilities (type: LOAN/OTHER, amount, description, owned_by)",
            "crime_cases": "criminal cases (FIR No, Police Station, Sections Applied, Charges Framed, description)",
        }

        for data_type in data_types:
            desc = descriptions.get(data_type, "")
            fmt = formats.get(data_type, "")
            query_parts.append(
                f"{data_type.capitalize()}: {desc}. Format: {fmt}"
            )

        combined_query = (
            f"Provide the following information about Indian politician {base_info}:\n\n"
            + "\n".join(f"{i+1}. {part}" for i, part in enumerate(query_parts))
            + "\n\n"
            "Search for this information using reliable sources like MyNeta.info. "
            "If information is not available for any section, return an empty list [] for that section. "
            "Return ONLY valid JSON objects, no markdown formatting, no code blocks, no other text. "
            "Do not include source citations or 'According to...' phrases in the values. "
            "Format the response as a JSON object with keys matching the data types above, "
            "each containing an array of objects."
        )

        return combined_query

    def _extract_json_from_response(self, response_text: str) -> Optional[Any]:
        """Extract JSON data from LLM response."""
        try:
            # Remove markdown code blocks if present
            match = re.search(r"```(?:json)?\s*(.*?)```", response_text, re.DOTALL)
            if match:
                response_text = match.group(1)

            response_text = response_text.strip()

            # Try to parse directly
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                pass

            # Fallback: find array or object
            start_idx_list = response_text.find("[")
            end_idx_list = response_text.rfind("]")
            start_idx_dict = response_text.find("{")
            end_idx_dict = response_text.rfind("}")

            if start_idx_list != -1 and end_idx_list != -1:
                if start_idx_dict == -1 or start_idx_list < start_idx_dict:
                    json_str = response_text[start_idx_list : end_idx_list + 1]
                    return json.loads(json_str)

            if start_idx_dict != -1 and end_idx_dict != -1:
                json_str = response_text[start_idx_dict : end_idx_dict + 1]
                return json.loads(json_str)

            return None
        except Exception as e:
            logger.warning(f"Failed to parse JSON from response: {e}")
            logger.debug(f"Raw response: {response_text[:200]}...")
            return None

    def _fetch_batch_data(
        self, candidate: Candidate, data_types: List[str]
    ) -> Dict[str, Optional[List[Dict[str, Any]]]]:
        """
        Fetch multiple data types in a single API call.

        This is the main optimization - reduces 6 API calls to 1.

        Args:
            candidate: Candidate object
            data_types: List of data types to fetch

        Returns:
            Dict mapping data_type to extracted data (or None if failed)
        """
        query = self._create_batch_query(candidate, data_types)

        # Check cache first
        if self.cache:
            cached = self.cache.get(query)
            if cached:
                logger.info(f"Using cached response for {candidate.name}")
                response_text = cached.get("answer", "")
            else:
                result = self.search_service.search_india(query)
                if result.get("error"):
                    logger.error(f"LLM error: {result['error']}")
                    return {dt: None for dt in data_types}
                response_text = result.get("answer", "")
                # Cache the response
                self.cache.set(query, result)
        else:
            result = self.search_service.search_india(query)
            if result.get("error"):
                logger.error(f"LLM error: {result['error']}")
                return {dt: None for dt in data_types}
            response_text = result.get("answer", "")

        # Parse the combined response
        parsed = self._extract_json_from_response(response_text)

        results = {}
        for data_type in data_types:
            if isinstance(parsed, dict):
                # Response is a dict with keys matching data_types
                data = parsed.get(data_type, [])
            elif isinstance(parsed, list) and len(parsed) == len(data_types):
                # Response is a list in the same order as data_types
                idx = data_types.index(data_type)
                data = parsed[idx] if idx < len(parsed) else []
            else:
                # Fallback: try to extract from text
                data = None

            if data is None or (isinstance(data, list) and len(data) == 0):
                results[data_type] = None
            else:
                if isinstance(data, dict):
                    data = [data]
                results[data_type] = data

        return results

    def _validate_and_format_data(
        self,
        data_type: str,
        data: List[Dict[str, Any]],
        candidate_name: str,
    ) -> Optional[List[Dict[str, Any]]]:
        """Validate and format data using Pydantic schemas."""
        schemas = {
            "education": EducationDetails,
            "political": PoliticalHistory,
            "family": FamilyMember,
            "assets": AssetDetails,
            "liabilities": LiabilityDetails,
            "crime_cases": CrimeCaseDetails,
        }

        schema = schemas.get(data_type)
        if not schema:
            return None

        validated_data = []
        for item in data:
            try:
                validated_data.append(schema(**item).dict())
            except ValidationError as ve:
                logger.warning(
                    f"Skipping invalid {data_type} data for {candidate_name} - {item}: {ve}"
                )

        if validated_data:
            logger.info(
                f"✅ {data_type.capitalize()} data found for {candidate_name} ({len(validated_data)} records)"
            )
            return validated_data
        return None

    def populate_candidate_data(
        self,
        session: Session,
        candidate: Candidate,
        delay_between_requests: float = 1.0,  # Reduced delay since we batch
    ) -> Dict[str, bool]:
        """
        Populate all missing data fields for a candidate using batch queries.

        Args:
            session: Database session
            candidate: Candidate object to populate
            delay_between_requests: Delay in seconds (minimal since we batch)

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

        # Determine which fields need to be fetched
        fields_to_fetch = []
        field_mapping = {
            "education": "education_background",
            "political": "political_background",
            "family": "family_background",
            "assets": "assets",
            "liabilities": "liabilities",
            "crime_cases": "crime_cases",
        }

        for data_type, field_name in field_mapping.items():
            if getattr(candidate, field_name) is None:
                fields_to_fetch.append(data_type)
            else:
                logger.info(
                    f"⏭️  {data_type.capitalize()} data already exists for {candidate.name}"
                )
                status[data_type] = True

        if not fields_to_fetch:
            logger.info(f"✅ All data already exists for {candidate.name}")
            return status

        # Fetch all missing fields in a single batch query
        logger.info(
            f"Fetching {len(fields_to_fetch)} data types in batch: {', '.join(fields_to_fetch)}"
        )
        batch_results = self._fetch_batch_data(candidate, fields_to_fetch)

        # Validate and format each result
        update_data = {}
        for data_type in fields_to_fetch:
            data = batch_results.get(data_type)
            if data:
                validated = self._validate_and_format_data(
                    data_type, data, candidate.name
                )
                if validated:
                    field_name = field_mapping[data_type]
                    update_data[field_name] = validated
                    status[data_type] = True

        # Small delay before next candidate
        time.sleep(delay_between_requests)

        # Update candidate if we have new data
        if update_data:
            try:
                candidate.update(session, **update_data)
                session.commit()
                logger.info(
                    f"✅ Successfully updated {candidate.name} with {len(update_data)} fields"
                )

                # Sync to vector DB if enabled
                if self.enable_vector_db and self.vector_db_pipeline:
                    try:
                        if self.vector_db_pipeline.sync_candidate(candidate):
                            logger.info(f"🔍 Synced {candidate.name} to vector database")
                        else:
                            logger.warning(
                                f"⚠️  Failed to sync {candidate.name} to vector database"
                            )
                    except Exception as ve:
                        logger.warning(
                            f"⚠️  Vector DB sync error for {candidate.name}: {ve}"
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
        delay_between_requests: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Run the optimized agent to populate data for multiple candidates.

        Args:
            session: Database session
            batch_size: Number of candidates to process
            delay_between_candidates: Delay between processing candidates
            delay_between_requests: Delay between requests (minimal since we batch)

        Returns:
            Summary statistics
        """
        logger.info("\n" + "=" * 60)
        logger.info("🚀 Starting Optimized Candidate Data Population Agent")
        logger.info("=" * 60 + "\n")
        logger.info(f"Batch size: {batch_size}")
        logger.info(f"Delay between candidates: {delay_between_candidates}s")
        logger.info(f"Delay between requests: {delay_between_requests}s\n")

        candidates = self.find_candidates_needing_data(session, limit=batch_size)

        if not candidates:
            logger.info("✅ No candidates found needing data population")
            return {"total_processed": 0, "successful": 0, "partial": 0, "failed": 0}

        stats = {
            "total_processed": 0,
            "successful": 0,
            "partial": 0,
            "failed": 0,
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

            if idx < len(candidates):
                time.sleep(delay_between_candidates)

        logger.info("\n" + "=" * 60)
        logger.info("🎉 Optimized Agent Run Complete")
        logger.info("=" * 60 + "\n")
        logger.info(f"Total candidates processed: {stats['total_processed']}")
        logger.info(f"Fully populated (6/6 fields): {stats['successful']}")
        logger.info(f"Partially populated: {stats['partial']}")
        logger.info(f"Failed to populate: {stats['failed']}")
        logger.info("")

        return stats

