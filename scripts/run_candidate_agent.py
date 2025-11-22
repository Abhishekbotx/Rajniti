#!/usr/bin/env python3
"""
CLI script to run the Candidate Data Population Agent.

This script runs the agent to automatically populate detailed candidate information
using Perplexity AI. It connects to the database and processes candidates in batches.

Usage:
    python scripts/run_candidate_agent.py [--batch-size 10] [--delay 2.0]

Environment Variables:
    DATABASE_URL: PostgreSQL connection string (required)
    PERPLEXITY_API_KEY: Perplexity API key (required)
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
from app.services.candidate_agent import CandidateDataAgent

# Load environment variables
load_dotenv()

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "candidate_agent.log"

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
    required_vars = ["PERPLEXITY_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
        logger.error("Please set them in your .env file or environment")
        return False

    # DATABASE_URL is optional - if not set, agent will use JSON files
    if not os.getenv("DATABASE_URL"):
        logger.warning("DATABASE_URL not set - make sure database is configured")
        logger.warning("The agent requires a database connection to work")
        return False

    return True


def main():
    """Main function to run the candidate data population agent."""
    parser = argparse.ArgumentParser(
        description="Run the Candidate Data Population Agent"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of candidates to process in one run (default: 10)",
    )
    parser.add_argument(
        "--delay-between-candidates",
        type=float,
        default=2.0,
        help="Delay in seconds between processing candidates (default: 2.0)",
    )
    parser.add_argument(
        "--delay-between-requests",
        type=float,
        default=2.0,
        help="Delay in seconds between API requests for same candidate (default: 2.0)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (no database updates)",
    )

    args = parser.parse_args()

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    logger.info("🚀 Candidate Data Population Agent")
    logger.info("=" * 60)
    logger.info(f"Batch size: {args.batch_size}")
    logger.info(f"Delay between candidates: {args.delay_between_candidates}s")
    logger.info(f"Delay between requests: {args.delay_between_requests}s")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info("=" * 60)
    logger.info("")

    try:
        # Initialize agent
        agent = CandidateDataAgent()

        # Run agent with database session
        with get_db_session() as session:
            if args.dry_run:
                logger.info("DRY RUN MODE - No database updates will be made")
                logger.info("")
                # Just find and display candidates
                candidates = agent.find_candidates_needing_data(
                    session, limit=args.batch_size
                )
                logger.info(f"Found {len(candidates)} candidates needing data:")
                for idx, candidate in enumerate(candidates, 1):
                    logger.info(f"{idx}. {candidate.name} (ID: {candidate.id})")
                logger.info("")
            else:
                agent.run(
                    session=session,
                    batch_size=args.batch_size,
                    delay_between_candidates=args.delay_between_candidates,
                    delay_between_requests=args.delay_between_requests,
                )

                logger.info("✅ Agent run completed successfully")
                logger.info("")
                logger.info("To process more candidates, run this script again.")
                logger.info(
                    "The agent will automatically find the next batch of candidates."
                )

    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Agent interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n\n❌ Agent failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
