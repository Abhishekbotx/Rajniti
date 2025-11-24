#!/usr/bin/env python3
"""
CLI script to sync candidate data to ChromaDB vector database.

This script syncs candidate information from the PostgreSQL database
to ChromaDB for semantic search capabilities. It can run in full sync
mode or incremental mode.

Usage:
    # Full sync - sync all candidates
    python scripts/sync_candidates_to_vector_db.py

    # Sync with batch size
    python scripts/sync_candidates_to_vector_db.py --batch-size 50

    # Sync only winners
    python scripts/sync_candidates_to_vector_db.py --winners-only

    # Sync specific state
    python scripts/sync_candidates_to_vector_db.py --state DL

Environment Variables:
    DATABASE_URL: PostgreSQL connection string (required)
    CHROMA_DB_PATH: Path to ChromaDB storage (optional, defaults to data/chroma_db)
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

from app.database import get_db_session
from app.services.vector_db_pipeline import VectorDBPipeline

# Load environment variables
load_dotenv()

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "vector_db_sync.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)


def validate_environment():
    """Validate required environment variables are set."""
    # DATABASE_URL is optional - if not set, script will warn
    if not os.getenv("DATABASE_URL"):
        logger.warning("DATABASE_URL not set - make sure database is configured")
        logger.warning("The sync requires a database connection to work")
        return False

    return True


def main():
    """Main function to sync candidates to vector database."""
    parser = argparse.ArgumentParser(
        description="Sync candidate data to ChromaDB vector database"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of candidates to process in one batch (default: 100)",
    )
    parser.add_argument(
        "--winners-only",
        action="store_true",
        help="Sync only winning candidates",
    )
    parser.add_argument(
        "--state",
        type=str,
        help="Sync only candidates from specific state (e.g., DL, MH)",
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["MP", "MLA"],
        help="Sync only specific candidate type (MP or MLA)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (show what would be synced without syncing)",
    )

    args = parser.parse_args()

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    logger.info("🚀 Candidate to Vector DB Sync")
    logger.info("=" * 60)
    logger.info(f"Batch size: {args.batch_size}")
    logger.info(f"Winners only: {args.winners_only}")
    logger.info(f"State filter: {args.state or 'All'}")
    logger.info(f"Type filter: {args.type or 'All'}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info(f"ChromaDB path: {os.getenv('CHROMA_DB_PATH', 'data/chroma_db')}")
    logger.info("=" * 60)
    logger.info("")

    try:
        # Initialize pipeline
        pipeline = VectorDBPipeline()

        # Build filter criteria
        filter_criteria = {}
        if args.winners_only:
            filter_criteria["status"] = "WON"
        if args.state:
            filter_criteria["state_id"] = args.state
        if args.type:
            filter_criteria["type"] = args.type

        # Run sync with database session
        with get_db_session() as session:
            if args.dry_run:
                logger.info("DRY RUN MODE - No data will be synced")
                logger.info("")
                
                # Count candidates that would be synced
                from app.database.models import Candidate
                query = session.query(Candidate)
                
                if filter_criteria.get("status"):
                    query = query.filter(Candidate.status == filter_criteria["status"])
                if filter_criteria.get("state_id"):
                    query = query.filter(Candidate.state_id == filter_criteria["state_id"])
                if filter_criteria.get("type"):
                    query = query.filter(Candidate.type == filter_criteria["type"])
                
                count = query.count()
                logger.info(f"Would sync {count} candidates based on filters")
                logger.info("")
            else:
                stats = pipeline.sync_all_candidates(
                    session=session,
                    batch_size=args.batch_size,
                    filter_criteria=filter_criteria if filter_criteria else None
                )

                logger.info("")
                logger.info("✅ Sync completed successfully")
                logger.info("=" * 60)
                logger.info(f"Total candidates processed: {stats['total']}")
                logger.info(f"Successfully synced: {stats['synced']}")
                logger.info(f"Failed: {stats['failed']}")
                logger.info(f"Batches: {stats['batches']}")
                logger.info("=" * 60)
                logger.info("")
                logger.info("Vector database is now ready for semantic search!")
                
                # Show current vector DB stats
                total_in_db = pipeline.vector_db.count_candidates()
                logger.info(f"Total candidates in vector database: {total_in_db}")

    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Sync interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n\n❌ Sync failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
