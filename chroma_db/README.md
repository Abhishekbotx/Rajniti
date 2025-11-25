# ChromaDB Vector Database

This directory contains the ChromaDB vector database used for semantic search across candidate information.

## What's Inside

- **`chroma.sqlite3`**: The ChromaDB database file containing:
  - Vector embeddings of candidate data
  - Document metadata (name, party, constituency, etc.)
  - Collection information
  - Index data for fast similarity search

## Storage Format

ChromaDB uses **SQLite** as its persistent storage backend. This is the standard and expected behavior:
- The `.sqlite3` file format is correct - ChromaDB doesn't have its own proprietary format
- SQLite provides reliable, ACID-compliant local persistence
- The database can be inspected using standard SQLite tools

## Usage

The database is automatically created and populated when:
- Running the candidate agent: `python scripts/run_candidate_agent.py`
- Running the sync script: `python scripts/sync_candidates_to_vector_db.py`

## Configuration

The database path can be configured via the `CHROMA_DB_PATH` environment variable:
```bash
export CHROMA_DB_PATH="data/chroma_db"  # default
```

## For Developers

### Inspecting the Database

You can inspect the database using SQLite tools:
```bash
sqlite3 chroma_db/chroma.sqlite3
.tables
.schema
```

### Resetting the Database

To start fresh, simply delete the `chroma.sqlite3` file. It will be recreated on the next run.

### Note on Version Control

This database file is tracked in git for documentation and development purposes. In production, you may want to:
- Use a separate database path outside the repository
- Exclude it from version control
- Use ChromaDB's server mode for production deployments

## Related Documentation

- [Vector DB Documentation](../docs/VECTOR_DB.md)
- [ChromaDB Official Docs](https://docs.trychroma.com/)

