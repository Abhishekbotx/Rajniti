# Database Layer Documentation

This directory contains the database layer for Rajniti Election Data API.

## Overview

The database layer provides:
- **DB Models** with CRUD operations for Party, Constituency, and Candidate
- **PostgreSQL Support** compatible with both local PostgreSQL and Supabase
- **Alembic Migrations** for database schema management
- **JSON to DB Migration** script to migrate existing JSON data

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

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Full database connection string | `postgresql://user:pass@host:5432/db` |
| `SUPABASE_DB_URL` | Supabase database URL | `postgresql://postgres:pass@db.xxx.supabase.co:5432/postgres` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `rajniti` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |
| `DB_ECHO` | Log SQL queries | `true` or `false` |

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
