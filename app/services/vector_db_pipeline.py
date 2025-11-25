"""
Vector Database Pipeline Service

This service orchestrates the ingestion of candidate data into ChromaDB
for semantic search capabilities. It converts candidate information from
the database into text embeddings and stores them in the vector database.
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.database.models import Candidate
from app.services.vector_db_service import VectorDBService

logger = logging.getLogger(__name__)


class VectorDBPipeline:
    """
    Pipeline for syncing candidate data from the database to ChromaDB.

    This pipeline:
    1. Fetches candidates from the database
    2. Converts candidate information to searchable text format
    3. Stores the text and metadata in ChromaDB for semantic search
    """

    def __init__(self, vector_db_service: Optional[VectorDBService] = None):
        """
        Initialize the VectorDB pipeline.

        Args:
            vector_db_service: Optional VectorDBService instance.
                             If not provided, a new instance will be created.
        """
        self.vector_db = vector_db_service or VectorDBService(
            collection_name="candidates"
        )
        logger.info("VectorDBPipeline initialized successfully")

    def _candidate_to_text(self, candidate: Candidate) -> str:
        """
        Convert candidate data to searchable text format.

        Args:
            candidate: Candidate database model instance

        Returns:
            String representation of candidate for embedding
        """
        text_parts = [
            f"Name: {candidate.name}",
            f"Constituency: {candidate.constituency_id}",
            f"State: {candidate.state_id}",
            f"Party: {candidate.party_id}",
            f"Status: {candidate.status}",
            f"Type: {candidate.type}",
        ]

        # Add education background
        if candidate.education_background:
            edu_text = []
            for edu in candidate.education_background:
                edu_parts = []
                if edu.get("year"):
                    edu_parts.append(f"graduated in {edu['year']}")
                if edu.get("stream"):
                    edu_parts.append(f"studied {edu['stream']}")
                if edu.get("college"):
                    edu_parts.append(f"from {edu['college']}")
                if edu.get("other_details"):
                    edu_parts.append(edu["other_details"])
                if edu_parts:
                    edu_text.append(" ".join(edu_parts))
            if edu_text:
                text_parts.append(f"Education: {'; '.join(edu_text)}")

        # Add political background
        if candidate.political_background:
            pol_text = []
            for pol in candidate.political_background:
                pol_parts = []
                if pol.get("election_year"):
                    pol_parts.append(f"In {pol['election_year']}")
                if pol.get("result"):
                    pol_parts.append(f"{pol['result'].lower()}")
                if pol.get("constituency"):
                    pol_parts.append(f"from {pol['constituency']}")
                if pol.get("party"):
                    pol_parts.append(f"with {pol['party']}")
                if pol.get("position"):
                    pol_parts.append(f"as {pol['position']}")
                if pol_parts:
                    pol_text.append(" ".join(pol_parts))
            if pol_text:
                text_parts.append(f"Political History: {'; '.join(pol_text)}")

        # Add family background
        if candidate.family_background:
            fam_text = []
            for fam in candidate.family_background:
                fam_parts = []
                if fam.get("name"):
                    fam_parts.append(fam["name"])
                if fam.get("relation"):
                    fam_parts.append(f"({fam['relation']})")
                if fam.get("profession"):
                    fam_parts.append(f"is a {fam['profession']}")
                if fam_parts:
                    fam_text.append(" ".join(fam_parts))
            if fam_text:
                text_parts.append(f"Family: {'; '.join(fam_text)}")

        # Add assets summary
        if candidate.assets:
            total_assets = sum(asset.get("amount", 0) for asset in candidate.assets)
            asset_types = set(
                asset.get("type") for asset in candidate.assets if asset.get("type")
            )
            if total_assets > 0 or asset_types:
                asset_parts = []
                if total_assets > 0:
                    asset_parts.append(f"Total assets: ₹{total_assets:,.2f}")
                if asset_types:
                    asset_parts.append(f"Asset types: {', '.join(asset_types)}")
                text_parts.append(f"Assets: {'; '.join(asset_parts)}")

        # Add liabilities summary
        if candidate.liabilities:
            total_liabilities = sum(
                liability.get("amount", 0) for liability in candidate.liabilities
            )
            if total_liabilities > 0:
                text_parts.append(f"Liabilities: Total ₹{total_liabilities:,.2f}")

        # Add crime cases info
        if candidate.crime_cases:
            crime_count = len(candidate.crime_cases)
            charges_framed = sum(
                1 for case in candidate.crime_cases if case.get("charges_framed")
            )
            crime_parts = [f"{crime_count} criminal case(s)"]
            if charges_framed > 0:
                crime_parts.append(f"{charges_framed} with charges framed")
            text_parts.append(f"Criminal Cases: {'; '.join(crime_parts)}")

        return ". ".join(text_parts) + "."

    def _candidate_to_metadata(self, candidate: Candidate) -> Dict[str, Any]:
        """
        Extract metadata from candidate for filtering and retrieval.

        Args:
            candidate: Candidate database model instance

        Returns:
            Dictionary of metadata
        """
        metadata = {
            "candidate_id": candidate.id,
            "name": candidate.name,
            "party_id": candidate.party_id,
            "constituency_id": candidate.constituency_id,
            "state_id": candidate.state_id,
            "status": candidate.status,
            "type": candidate.type,
        }

        # Add optional fields
        if candidate.image_url:
            metadata["image_url"] = candidate.image_url

        # Add counts for detailed data
        if candidate.education_background:
            metadata["education_count"] = len(candidate.education_background)
        if candidate.political_background:
            metadata["political_history_count"] = len(candidate.political_background)
        if candidate.family_background:
            metadata["family_members_count"] = len(candidate.family_background)
        if candidate.assets:
            metadata["assets_count"] = len(candidate.assets)
        if candidate.crime_cases:
            metadata["crime_cases_count"] = len(candidate.crime_cases)

        return metadata

    def sync_candidate(self, candidate: Candidate) -> bool:
        """
        Sync a single candidate to the vector database.

        Args:
            candidate: Candidate database model instance

        Returns:
            True if successful, False otherwise
        """
        try:
            text = self._candidate_to_text(candidate)
            metadata = self._candidate_to_metadata(candidate)

            self.vector_db.upsert_candidate_data(
                candidate_id=candidate.id, text=text, metadata=metadata
            )
            logger.info(
                f"Successfully synced candidate {candidate.name} (ID: {candidate.id})"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to sync candidate {candidate.id}: {e}")
            return False

    def sync_candidates_batch(
        self,
        session: Session,
        batch_size: int = 100,
        offset: int = 0,
        filter_criteria: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, int]:
        """
        Sync a batch of candidates to the vector database.

        Args:
            session: Database session
            batch_size: Number of candidates to process in one batch
            offset: Number of candidates to skip
            filter_criteria: Optional filtering criteria (e.g., {"status": "WON"})

        Returns:
            Statistics dictionary with 'total', 'synced', 'failed'
        """
        logger.info(f"Starting batch sync: batch_size={batch_size}, offset={offset}")

        # Build query
        query = session.query(Candidate)

        # Apply filters if provided
        if filter_criteria:
            if filter_criteria.get("status"):
                query = query.filter(Candidate.status == filter_criteria["status"])
            if filter_criteria.get("state_id"):
                query = query.filter(Candidate.state_id == filter_criteria["state_id"])
            if filter_criteria.get("type"):
                query = query.filter(Candidate.type == filter_criteria["type"])

        # Get candidates
        candidates = query.offset(offset).limit(batch_size).all()

        stats = {"total": len(candidates), "synced": 0, "failed": 0}

        for candidate in candidates:
            if self.sync_candidate(candidate):
                stats["synced"] += 1
            else:
                stats["failed"] += 1

        logger.info(f"Batch sync completed: {stats}")
        return stats

    def sync_all_candidates(
        self,
        session: Session,
        batch_size: int = 100,
        filter_criteria: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, int]:
        """
        Sync all candidates to the vector database in batches.

        Args:
            session: Database session
            batch_size: Number of candidates to process in one batch
            filter_criteria: Optional filtering criteria

        Returns:
            Overall statistics dictionary
        """
        logger.info("Starting full sync of all candidates to vector database")

        overall_stats = {"total": 0, "synced": 0, "failed": 0, "batches": 0}

        offset = 0
        while True:
            batch_stats = self.sync_candidates_batch(
                session,
                batch_size=batch_size,
                offset=offset,
                filter_criteria=filter_criteria,
            )

            if batch_stats["total"] == 0:
                break

            overall_stats["total"] += batch_stats["total"]
            overall_stats["synced"] += batch_stats["synced"]
            overall_stats["failed"] += batch_stats["failed"]
            overall_stats["batches"] += 1

            offset += batch_size

            logger.info(
                f"Progress: {overall_stats['synced']}/{overall_stats['total']} candidates synced"
            )

        logger.info(f"Full sync completed: {overall_stats}")
        return overall_stats

    def delete_candidate(self, candidate_id: str) -> bool:
        """
        Delete a candidate from the vector database.

        Args:
            candidate_id: Unique identifier for the candidate

        Returns:
            True if successful, False otherwise
        """
        try:
            self.vector_db.delete_candidate(candidate_id)
            logger.info(f"Deleted candidate {candidate_id} from vector database")
            return True
        except Exception as e:
            logger.error(f"Failed to delete candidate {candidate_id}: {e}")
            return False
