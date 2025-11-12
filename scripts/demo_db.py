#!/usr/bin/env python
"""
Database Demo Script

Demonstrates the usage of database models with sample data.
This script shows how to use the database layer without requiring an actual database connection.

Usage:
    python scripts/demo_db.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def demo_models():
    """Demonstrate database models (without actual database)."""
    print("=" * 60)
    print("Database Models Demo")
    print("=" * 60)

    print("\n📋 Database Models Overview:\n")

    print("1. Party Model")
    print("   - Fields: id, name, short_name, symbol")
    print("   - CRUD Operations:")
    print("     • Party.create(session, id, name, short_name, symbol)")
    print("     • Party.get_by_id(session, party_id)")
    print("     • Party.get_by_name(session, name)")
    print("     • Party.get_all(session, skip=0, limit=100)")
    print("     • party.update(session, **kwargs)")
    print("     • party.delete(session)")
    print("     • Party.bulk_create(session, parties_list)")

    print("\n2. Constituency Model")
    print("   - Fields: id, name, state_id")
    print("   - CRUD Operations:")
    print("     • Constituency.create(session, id, name, state_id)")
    print("     • Constituency.get_by_id(session, constituency_id)")
    print("     • Constituency.get_by_state(session, state_id)")
    print("     • Constituency.get_all(session, skip=0, limit=100)")
    print("     • constituency.update(session, **kwargs)")
    print("     • constituency.delete(session)")
    print("     • Constituency.bulk_create(session, constituencies_list)")

    print("\n3. Candidate Model")
    print("   - Fields: id, name, party_id, constituency_id, state_id,")
    print("            status, type, image_url")
    print("   - CRUD Operations:")
    print("     • Candidate.create(session, id, name, party_id, ...)")
    print("     • Candidate.get_by_id(session, candidate_id)")
    print("     • Candidate.get_by_party(session, party_id)")
    print("     • Candidate.get_by_constituency(session, constituency_id)")
    print("     • Candidate.get_winners(session, skip=0, limit=100)")
    print("     • Candidate.search_by_name(session, name)")
    print("     • Candidate.get_all(session, skip=0, limit=100)")
    print("     • candidate.update(session, **kwargs)")
    print("     • candidate.delete(session)")
    print("     • Candidate.bulk_create(session, candidates_list)")


def demo_usage():
    """Demonstrate database usage patterns."""
    print("\n" + "=" * 60)
    print("Database Usage Examples")
    print("=" * 60)

    print("\n📝 Example 1: Creating a Party")
    print("-" * 60)
    print(
        """
from app.database import get_db_session
from app.database.models import Party

with get_db_session() as session:
    party = Party.create(
        session=session,
        id="123",
        name="Example Party",
        short_name="EP",
        symbol="Lotus"
    )
    print(f"Created: {party.name}")
"""
    )

    print("\n📝 Example 2: Searching Candidates")
    print("-" * 60)
    print(
        """
from app.database import get_db_session
from app.database.models import Candidate

with get_db_session() as session:
    # Search by name
    candidates = Candidate.search_by_name(session, "Modi")
    
    # Get winners only
    winners = Candidate.get_winners(session, skip=0, limit=10)
    
    # Get by party
    party_candidates = Candidate.get_by_party(session, "369")
"""
    )

    print("\n📝 Example 3: Bulk Operations")
    print("-" * 60)
    print(
        """
from app.database import get_db_session
from app.database.models import Party

parties_data = [
    {"id": "1", "name": "Party A", "short_name": "PA", "symbol": ""},
    {"id": "2", "name": "Party B", "short_name": "PB", "symbol": ""},
]

with get_db_session() as session:
    Party.bulk_create(session, parties_data)
    print(f"Created {len(parties_data)} parties")
"""
    )


def demo_migration():
    """Demonstrate migration process."""
    print("\n" + "=" * 60)
    print("Migration Process")
    print("=" * 60)

    print("\n🔄 Step 1: Setup Database")
    print("-" * 60)
    print("# Local PostgreSQL")
    print("createdb rajniti")
    print("export DATABASE_URL='postgresql://postgres:postgres@localhost:5432/rajniti'")
    print("")
    print("# Or Supabase")
    print(
        "export SUPABASE_DB_URL='postgresql://postgres:[pass]@db.[project].supabase.co:5432/postgres'"
    )

    print("\n🔄 Step 2: Initialize Database")
    print("-" * 60)
    print("python scripts/db.py init")

    print("\n🔄 Step 3: Migrate Data")
    print("-" * 60)
    print("# Preview migration")
    print("python scripts/db.py migrate --dry-run")
    print("")
    print("# Execute migration")
    print("python scripts/db.py migrate")

    print("\n🔄 Step 4: Verify Data")
    print("-" * 60)
    print(
        """
from app.database import get_db_session
from app.database.models import Party, Constituency, Candidate

with get_db_session() as session:
    party_count = len(Party.get_all(session))
    const_count = len(Constituency.get_all(session))
    cand_count = len(Candidate.get_all(session))
    
    print(f"Parties: {party_count}")
    print(f"Constituencies: {const_count}")
    print(f"Candidates: {cand_count}")
"""
    )


def demo_service():
    """Demonstrate database service usage."""
    print("\n" + "=" * 60)
    print("Database Service Usage")
    print("=" * 60)

    print("\n📊 Using Database Service")
    print("-" * 60)
    print(
        """
from app.services.db_data_service import DbDataService

service = DbDataService()

# Get all parties
parties = service.get_parties("lok-sabha-2024")

# Search candidates
candidates = service.search_candidates("Modi")

# Get candidate details (includes party and constituency info)
candidate = service.get_candidate_by_id("abc-123", "lok-sabha-2024")
print(f"{candidate['name']} - {candidate['party_name']}")
print(f"Constituency: {candidate['constituency_name']}")
"""
    )


def main():
    """Main entry point."""
    demo_models()
    demo_usage()
    demo_migration()
    demo_service()

    print("\n" + "=" * 60)
    print("📚 For full documentation, see:")
    print("   - app/database/README.md")
    print("   - readme.md (Database Support section)")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
