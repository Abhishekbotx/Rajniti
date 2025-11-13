# Database Layer Documentation

This directory contains the database layer for Rajniti Election Data API.

## Overview

The database layer provides:

-   **DB Models** with CRUD operations for Party, Constituency, and Candidate
-   **PostgreSQL Support** compatible with both local PostgreSQL and Supabase
-   **Alembic Migrations** for database schema management
-   **JSON to DB Migration** script to migrate existing JSON data

## Structure

```
app/database/
├── __init__.py           # Package exports
├── base.py               # Base model class and utilities
├── config.py             # Database configuration
├── session.py            # Database session management
└── models/               # Database models
    ├── __init__.py
    ├── party.py          # Party model with CRUD
    ├── constituency.py   # Constituency model with CRUD
    └── candidate.py      # Candidate model with CRUD
```

## Database Configuration

The application supports multiple ways to configure the database:

### Option 1: Full Database URL (Recommended)

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/rajniti
```

### Option 2: Supabase Database URL

```bash
SUPABASE_DB_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
```

### Option 3: Individual Components

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rajniti
DB_USER=postgres
DB_PASSWORD=postgres
```

## Setup

### 1. Local PostgreSQL Setup

```bash
# Install PostgreSQL (if not already installed)
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS (with Homebrew)
brew install postgresql

# Start PostgreSQL
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# Create database
createdb rajniti

# Or using psql
psql -U postgres
CREATE DATABASE rajniti;
\q
```

If Above doesn't work, You may not have your user created. Follow the steps below -

1. Connect via Default User

```
psql -d postgres
```

2. Check existing roles

```
\du
```

3. Create a New User with Password. Remember the password as You'll need for DB Connection

```
CREATE ROLE postgres WITH LOGIN SUPERUSER PASSWORD 'postgres';
```

4. Log in via newly created user

```
psql -U postgres -d postgres
```

5. Create DB

```
CREATE DATABASE rajniti;
```

### 2. Supabase Setup

1. Create a Supabase project at https://supabase.com
2. Get your database connection string from:
    - Project Settings → Database → Connection String
    - Use the "URI" format
3. Set the `SUPABASE_DB_URL` environment variable

### 3. Initialize Database

```bash
# Activate virtual environment
source venv/bin/activate

# Set database URL (choose one method)
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rajniti"
# OR
export SUPABASE_DB_URL="postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres"

# Initialize database (creates tables)
python -c "from app.database import init_db; init_db()"
```

## Database Migrations

We use Alembic for database schema migrations.

### Create a New Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Create empty migration template
alembic revision -m "description of changes"
```

### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade +1

# Downgrade one migration
alembic downgrade -1
```

### View Migration History

```bash
# Show current migration
alembic current

# Show migration history
alembic history
```

### Migration Workflow

When you make changes to database models, follow this workflow:

**Important**: Always commit migration files (`alembic/versions/*.py`) to git. These files are essential for:

-   Team collaboration (everyone needs the same migration history)
-   Production deployments (migrations must run in order)
-   Database schema version control
-   Rollback capabilities

#### Step 1: Check Current Status

```bash
# Check if database is up to date
alembic current

# View migration history
alembic history
```

#### Step 2: Create Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# This will create a migration file in alembic/versions/
```

**Important**: Review the generated migration file before applying it. You may need to:

-   Add data migration logic for existing records
-   Handle nullable columns properly (add as nullable first, populate data, then make NOT NULL)
-   Add custom SQL for complex transformations

#### Step 3: Review Migration File

Always review the auto-generated migration file (`alembic/versions/XXXXX_description.py`):

-   Check that all model changes are captured correctly
-   Add data migration steps if needed (e.g., populating new columns from existing data)
-   Ensure backward compatibility if removing columns
-   Test the migration on a copy of production data if possible

#### Step 4: Apply Migration

```bash
# Apply the migration
alembic upgrade head

# Verify migration was applied
alembic current
```

#### Step 5: Verify Migration

After applying a migration, verify it worked correctly:

##### 5.1: Check Alembic Status

```bash
# Check current migration version
alembic current
# Should show the latest migration revision (e.g., 2b1da9ee1f5d (head))

# View migration history
alembic history
# Should show all migrations including the one you just applied
```

##### 5.2: Verify Database Schema (Using psql)

**Connect to Database:**

```bash
# Connect using connection string
psql "postgresql://postgres:postgres@localhost:5432/rajniti"

# Or if using environment variable
psql $DATABASE_URL

# Or connect step by step
psql -U postgres -d rajniti
```

**List All Tables:**

```sql
-- List all tables in the database
\dt

-- Or get more details
\dt+

-- List tables with schema information
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

**Check Table Structure:**

```sql
-- Describe a specific table (shows columns, types, constraints)
\d constituencies

-- Or get detailed information
\d+ constituencies

-- Get column information using SQL
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'constituencies'
ORDER BY ordinal_position;
```

**View Table Data:**

```sql
-- View first 10 rows
SELECT * FROM constituencies LIMIT 10;

-- Count total rows
SELECT COUNT(*) FROM constituencies;

-- View specific columns
SELECT id, original_id, name, state_id
FROM constituencies
LIMIT 5;

-- Check for NULL values in new columns
SELECT
    COUNT(*) as total,
    COUNT(original_id) as with_original_id,
    COUNT(*) - COUNT(original_id) as missing_original_id
FROM constituencies;
```

**Verify Migration-Specific Changes:**

```sql
-- Check if new columns exist
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'constituencies'
  AND column_name IN ('original_id', 'id', 'name', 'state_id');

-- Verify data was migrated correctly (if applicable)
SELECT id, original_id, name, state_id
FROM constituencies
WHERE original_id IS NULL;  -- Should return 0 rows

-- Check candidates table
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'candidates'
  AND column_name IN ('original_constituency_id', 'constituency_id', 'state_id');

-- Exit psql
\q
```

##### 5.3: Verify Using Python

```python
from app.database import get_db_session
from app.database.models import Constituency, Candidate
from sqlalchemy import inspect, text

# Verify table structure
with get_db_session() as session:
    # Check Constituency table columns
    inspector = inspect(Constituency)
    constituency_columns = [col.name for col in inspector.columns]
    print("Constituency columns:", constituency_columns)

    # Check Candidate table columns
    inspector = inspect(Candidate)
    candidate_columns = [col.name for col in inspector.columns]
    print("Candidate columns:", candidate_columns)

    # Count records
    constituency_count = session.query(Constituency).count()
    candidate_count = session.query(Candidate).count()
    print(f"\nTotal constituencies: {constituency_count}")
    print(f"Total candidates: {candidate_count}")

    # View sample data
    if constituency_count > 0:
        sample = session.query(Constituency).first()
        print(f"\nSample constituency:")
        print(f"  id: {sample.id}")
        print(f"  original_id: {sample.original_id}")
        print(f"  name: {sample.name}")
        print(f"  state_id: {sample.state_id}")

print("\n✓ Migration verification complete!")
```

##### 5.4: Common Verification Queries

**Check All Tables:**

```sql
-- List all tables with row counts
SELECT
    schemaname,
    tablename,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = tablename) as column_count
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

**Verify Foreign Key Relationships:**

```sql
-- Check foreign key constraints
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public';
```

**Check Indexes:**

```sql
-- List all indexes
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

**Data Integrity Checks:**

```sql
-- Verify no orphaned records (if foreign keys exist)
SELECT COUNT(*) as orphaned_candidates
FROM candidates c
LEFT JOIN constituencies const ON c.constituency_id = const.id
WHERE const.id IS NULL;

-- Check for duplicate primary keys (should return 0)
SELECT id, COUNT(*)
FROM constituencies
GROUP BY id
HAVING COUNT(*) > 1;
```

##### 5.5: Quick Verification Checklist

After running a migration, verify:

-   [ ] `alembic current` shows the new migration revision
-   [ ] New columns exist in the target table(s)
-   [ ] Column data types are correct
-   [ ] NOT NULL constraints are applied (if applicable)
-   [ ] Existing data is preserved (if applicable)
-   [ ] New columns are populated (if data migration was needed)
-   [ ] No errors in application logs
-   [ ] Application can query the updated tables successfully

#### Common Errors and Solutions

**Error**: `Target database is not up to date`

-   **Cause**: There's an unapplied migration
-   **Solution**: Run `alembic upgrade head` first to apply pending migrations, then create new migrations

**Error**: `Can't locate revision identified by 'XXXXX'`

-   **Cause**: Migration history mismatch between database and files
-   **Solution**: Check `alembic current` vs `alembic history` to identify the issue

**Error**: Column already exists / Column does not exist

-   **Cause**: Database schema doesn't match expected state
-   **Solution**:
    -   Check migration history: `alembic history`
    -   Verify current state: `alembic current`
    -   If needed, reset: `alembic downgrade base && alembic upgrade head` (⚠️ deletes all data)

#### Handling Existing Data

When adding new columns to existing tables with data:

1. Add column as nullable first
2. Populate data from existing columns or default values
3. Make column NOT NULL if required

Example migration pattern:

```python
def upgrade() -> None:
    # Step 1: Add column as nullable
    op.add_column('table_name', sa.Column('new_column', sa.String(), nullable=True))

    # Step 2: Populate data
    op.execute("""
        UPDATE table_name
        SET new_column = existing_column || '-suffix'
        WHERE new_column IS NULL
    """)

    # Step 3: Make NOT NULL (if required)
    op.alter_column('table_name', 'new_column', nullable=False)
```

#### Rollback Migration

```bash
# Rollback last migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations (⚠️ deletes all data)
alembic downgrade base
```

## Migrating JSON Data to Database

A migration script is provided to import existing JSON data into the database.

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Set database URL
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rajniti"

# Run migration (default: Lok Sabha 2024 data)
python scripts/migrations/migrate_json_to_db.py
```

### Advanced Usage

```bash
# Dry run (see what would be done without making changes)
python scripts/migrations/migrate_json_to_db.py --dry-run

# Migrate specific election data
python scripts/migrations/migrate_json_to_db.py --election-dir app/data/lok_sabha/lok-sabha-2024

# Migrate Vidhan Sabha data (if available)
python scripts/migrations/migrate_json_to_db.py --election-dir app/data/vidhan_sabha/DL_2025_ASSEMBLY
```

## Using Database Models

### Party Model

```python
from app.database import get_db_session
from app.database.models import Party

# Create a party
with get_db_session() as session:
    party = Party.create(
        session=session,
        id="123",
        name="Example Party",
        short_name="EP",
        symbol="Lotus"
    )

# Get party by ID
with get_db_session() as session:
    party = Party.get_by_id(session, "123")
    print(party.name)

# Get all parties
with get_db_session() as session:
    parties = Party.get_all(session, skip=0, limit=100)

# Update party
with get_db_session() as session:
    party = Party.get_by_id(session, "123")
    party.update(session, symbol="Elephant")

# Delete party
with get_db_session() as session:
    party = Party.get_by_id(session, "123")
    party.delete(session)
```

### Constituency Model

```python
from app.database import get_db_session
from app.database.models import Constituency

# Create a constituency
with get_db_session() as session:
    const = Constituency.create(
        session=session,
        id="1",
        name="New Delhi",
        state_id="DL"
    )

# Get constituency by state
with get_db_session() as session:
    constituencies = Constituency.get_by_state(session, "DL")
```

### Candidate Model

```python
from app.database import get_db_session
from app.database.models import Candidate

# Create a candidate
with get_db_session() as session:
    candidate = Candidate.create(
        session=session,
        id="abc-123",
        name="John Doe",
        party_id="123",
        constituency_id="1",
        state_id="DL",
        status="WON",
        type="MP",
        image_url="https://example.com/photo.jpg"
    )

# Search candidates by name
with get_db_session() as session:
    candidates = Candidate.search_by_name(session, "John")

# Get winners
with get_db_session() as session:
    winners = Candidate.get_winners(session, skip=0, limit=100)

# Get candidates by party
with get_db_session() as session:
    candidates = Candidate.get_by_party(session, "123")
```

## Bulk Operations

All models support bulk creation for efficient data loading:

```python
from app.database import get_db_session
from app.database.models import Party, Constituency, Candidate

# Bulk create parties
parties_data = [
    {"id": "1", "name": "Party A", "short_name": "PA", "symbol": ""},
    {"id": "2", "name": "Party B", "short_name": "PB", "symbol": ""},
]

with get_db_session() as session:
    Party.bulk_create(session, parties_data)
```

## Database Service Layer (Future Enhancement)

To integrate the database with the existing API, you can create a database service:

```python
# app/services/db_data_service.py
from app.database import get_db_session
from app.database.models import Party, Constituency, Candidate
from app.services.data_service import DataService

class DbDataService(DataService):
    """Database-backed data service implementation."""

    def get_parties(self, election_id: str):
        with get_db_session() as session:
            return Party.get_all(session)

    # Implement other DataService methods...
```

## Quick Reference: Database Operations

### Common psql Commands

```bash
# Connect to database
psql "postgresql://user:password@host:port/database"
psql -U username -d database_name

# List all databases
\l

# Connect to a specific database
\c database_name

# List all tables
\dt

# Describe a table structure
\d table_name
\d+ table_name  # More detailed

# List all columns in a table
\d+ table_name

# Show table size
\dt+ table_name

# List all schemas
\dn

# Show current database
SELECT current_database();

# Show current user
SELECT current_user;

# Exit psql
\q
```

### Common SQL Queries

```sql
-- Count rows in a table
SELECT COUNT(*) FROM table_name;

-- View all data (limit results)
SELECT * FROM table_name LIMIT 10;

-- View specific columns
SELECT column1, column2 FROM table_name;

-- Filter data
SELECT * FROM table_name WHERE column_name = 'value';

-- Sort results
SELECT * FROM table_name ORDER BY column_name DESC;

-- Group and aggregate
SELECT state_id, COUNT(*)
FROM constituencies
GROUP BY state_id;

-- Join tables
SELECT c.name, p.name as party_name
FROM candidates c
JOIN parties p ON c.party_id = p.id
LIMIT 10;
```

### Check Database Connection

```bash
# Test connection from command line
psql $DATABASE_URL -c "SELECT version();"

# Test using Python
python -c "from app.database.config import get_database_url; print(get_database_url())"
```

## Troubleshooting

### Connection Issues

```bash
# Test database connection
python -c "from app.database.config import get_database_url; print(get_database_url())"

# Test with psql
psql "postgresql://postgres:postgres@localhost:5432/rajniti"
```

### Migration Issues

```bash
# Reset database (WARNING: deletes all data)
alembic downgrade base
alembic upgrade head

# Or drop and recreate
dropdb rajniti
createdb rajniti
python -c "from app.database import init_db; init_db()"
```

### Permission Issues

```bash
# Grant permissions to user
psql -U postgres
GRANT ALL PRIVILEGES ON DATABASE rajniti TO your_user;
\q
```

## Environment Variables Reference

| Variable          | Description                     | Example                                                       |
| ----------------- | ------------------------------- | ------------------------------------------------------------- |
| `DATABASE_URL`    | Full database connection string | `postgresql://user:pass@host:5432/db`                         |
| `SUPABASE_DB_URL` | Supabase database URL           | `postgresql://postgres:pass@db.xxx.supabase.co:5432/postgres` |
| `DB_HOST`         | Database host                   | `localhost`                                                   |
| `DB_PORT`         | Database port                   | `5432`                                                        |
| `DB_NAME`         | Database name                   | `rajniti`                                                     |
| `DB_USER`         | Database user                   | `postgres`                                                    |
| `DB_PASSWORD`     | Database password               | `postgres`                                                    |
| `DB_ECHO`         | Log SQL queries                 | `true` or `false`                                             |

## Security Considerations

1. **Never commit database credentials** to version control
2. Use **environment variables** for all sensitive data
3. For production, use **strong passwords** and **SSL connections**
4. For Supabase, enable **Row Level Security (RLS)** policies
5. Regularly **backup your database**

## Performance Tips

1. Use **bulk operations** for large data imports
2. Add **indexes** on frequently queried columns (already done for key fields)
3. Use **connection pooling** (already configured in session.py)
4. For large datasets, use **pagination** with skip/limit parameters
5. Consider **caching** frequently accessed data
