# Vector Database Integration for Semantic Search

This document describes the ChromaDB vector database integration for storing and searching candidate information using semantic search capabilities.

## Overview

The vector database integration enables semantic search across candidate information by converting candidate data into text embeddings and storing them in ChromaDB. This allows for natural language queries to find relevant candidates based on their education, political history, family background, assets, and more.

## Architecture

### Components

1. **VectorDBService** (`app/services/vector_db_service.py`)
   - Low-level interface to ChromaDB
   - Handles CRUD operations for candidate embeddings
   - Manages persistent storage

2. **VectorDBPipeline** (`app/services/vector_db_pipeline.py`)
   - Orchestrates candidate data ingestion
   - Converts candidate data to searchable text
   - Provides batch and full sync operations

3. **CandidateDataAgent Integration** (`app/services/candidate_agent.py`)
   - Automatically syncs candidates to vector DB after populating data
   - Optional - can be disabled via `enable_vector_db=False`

4. **Sync Script** (`scripts/sync_candidates_to_vector_db.py`)
   - CLI tool for manual/periodic syncing
   - Supports filtering and batch processing

## Usage

### Automatic Sync (Recommended)

The candidate agent automatically syncs data to vector DB when populating candidate information:

```bash
# Runs agent and auto-syncs to vector DB
python scripts/run_candidate_agent.py --batch-size 10

# Disable auto-sync if needed
python scripts/run_candidate_agent.py --disable-vector-db
```

### Manual Sync

Use the sync script for periodic updates or initial data load:

```bash
# Sync all candidates
python scripts/sync_candidates_to_vector_db.py

# Sync only winners
python scripts/sync_candidates_to_vector_db.py --winners-only

# Sync specific state
python scripts/sync_candidates_to_vector_db.py --state DL

# Dry run to preview
python scripts/sync_candidates_to_vector_db.py --dry-run
```

### Programmatic Usage

```python
from app.database import get_db_session
from app.services.vector_db_pipeline import VectorDBPipeline

# Initialize pipeline
pipeline = VectorDBPipeline()

# Sync all candidates
with get_db_session() as session:
    stats = pipeline.sync_all_candidates(session, batch_size=100)
    print(f"Synced {stats['synced']} candidates")
```

## Configuration

### Environment Variables

- `CHROMA_DB_PATH`: Path to ChromaDB storage directory (default: `data/chroma_db`)
- `DATABASE_URL`: PostgreSQL connection string (required for sync operations)

## Testing

```bash
export DATABASE_URL="postgresql://test:test@localhost:5432/test"
pytest tests/test_vector_db_pipeline.py -v
```

For complete documentation, see the full VECTOR_DB.md in this directory.
