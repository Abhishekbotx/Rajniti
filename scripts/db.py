#!/usr/bin/env python
"""
Database management utility script.

Provides easy commands for common database operations.

Usage:
    python scripts/db.py init           # Initialize database (create tables)
    python scripts/db.py migrate        # Migrate JSON data to database
    python scripts/db.py migrate --dry-run  # Preview migration without changes
    python scripts/db.py reset          # Reset database (drop and recreate tables)
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db
from app.database.base import Base
from app.database.session import engine


def cmd_init():
    """Initialize database (create all tables)."""
    print("Initializing database...")
    try:
        init_db()
        print("✓ Database initialized successfully!")
        print("  All tables created.")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)


def cmd_reset():
    """Reset database (drop all tables and recreate)."""
    print("⚠️  WARNING: This will delete ALL data in the database!")
    response = input("Are you sure you want to continue? (yes/no): ")

    if response.lower() != "yes":
        print("Reset cancelled.")
        return

    print("\nResetting database...")
    try:
        # Drop all tables
        print("  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("  ✓ Tables dropped")

        # Recreate all tables
        print("  Creating tables...")
        init_db()
        print("  ✓ Tables created")

        print("\n✓ Database reset successfully!")
    except Exception as e:
        print(f"✗ Error resetting database: {e}")
        sys.exit(1)


def cmd_migrate(dry_run: bool = False, election_dir: Path = None):
    """Migrate JSON data to database."""
    from scripts.migrations.migrate_json_to_db import migrate_election_data

    if election_dir is None:
        election_dir = Path("app/data/lok_sabha/lok-sabha-2024")

    migrate_election_data(election_dir, dry_run)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Database management utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Init command
    subparsers.add_parser("init", help="Initialize database (create tables)")

    # Reset command
    subparsers.add_parser("reset", help="Reset database (drop and recreate tables)")

    # Migrate command
    migrate_parser = subparsers.add_parser("migrate", help="Migrate JSON data to database")
    migrate_parser.add_argument(
        "--dry-run", action="store_true", help="Preview without making changes"
    )
    migrate_parser.add_argument(
        "--election-dir",
        type=Path,
        help="Path to election data directory",
    )

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "reset":
        cmd_reset()
    elif args.command == "migrate":
        cmd_migrate(args.dry_run, args.election_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
