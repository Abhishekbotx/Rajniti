# Candidate Data Population Agent

An automated agent system that populates detailed candidate information using Perplexity AI.

## Overview

The Candidate Data Population Agent is a background service that automatically:

1. Finds candidates with missing detailed information in the database
2. Uses Perplexity AI to fetch structured data about each candidate
3. Updates the database with the fetched information
4. Continues until all candidates have complete data

## Features

-   **Automatic Discovery**: Finds candidates missing education, political, family, or asset information
-   **Structured Data Extraction**: Uses Perplexity AI with JSON-formatted prompts for consistent data
-   **Incremental Updates**: Processes candidates in batches to manage API usage
-   **Error Handling**: Gracefully handles API failures and missing data
-   **Progress Tracking**: Detailed logging of all operations
-   **Rate Limiting**: Built-in delays to respect API rate limits

## Architecture

The agent consists of two main components:

### 1. CandidateDataAgent (`app/services/candidate_agent.py`)

The core agent class that handles:

-   Finding candidates needing data
-   Creating Perplexity queries for each data field
-   Extracting JSON from Perplexity responses
-   Updating the database

### 2. CLI Script (`scripts/run_candidate_agent.py`)

Command-line interface for running the agent with:

-   Configurable batch sizes
-   Adjustable delays
-   Dry-run mode for testing
-   Environment validation

## Prerequisites

### 1. Database Setup

You need a PostgreSQL database with the candidate tables. If not already set up:

```bash
# Set DATABASE_URL in .env file
DATABASE_URL=postgresql://user:password@localhost:5432/rajniti

# Run migrations
python scripts/db.py sync
```

### 2. Perplexity API Key

Get your API key from [Perplexity AI](https://www.perplexity.ai/):

```bash
# Add to .env file
PERPLEXITY_API_KEY=your-api-key-here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Process 10 candidates with default settings:

```bash
python scripts/run_candidate_agent.py
```

### Custom Batch Size

Process 50 candidates at once:

```bash
python scripts/run_candidate_agent.py --batch-size 50
```

### Adjust Delays

Customize delays to manage API rate limits:

```bash
python scripts/run_candidate_agent.py \
  --batch-size 20 \
  --delay-between-candidates 3.0 \
  --delay-between-requests 2.5
```

### Dry Run

Test without making database updates:

```bash
python scripts/run_candidate_agent.py --dry-run
```

This will show which candidates would be processed without actually calling the API or updating the database.

### All Options

```bash
python scripts/run_candidate_agent.py --help
```

Options:

-   `--batch-size`: Number of candidates to process (default: 10)
-   `--delay-between-candidates`: Seconds between processing candidates (default: 2.0)
-   `--delay-between-requests`: Seconds between API requests for same candidate (default: 2.0)
-   `--dry-run`: Run without making changes

## How It Works

### 1. Find Candidates

The agent queries the database for candidates where any of these fields are `NULL`:

-   `education_background`
-   `family_background`
-   `assets`

### 2. Fetch Data

For each candidate, the agent:

1. Creates a structured query asking Perplexity for data in JSON format
2. Calls Perplexity AI's search API
3. Extracts the JSON data from the response
4. Validates the structure

### 3. Update Database

The agent:

1. Only updates fields that were successfully fetched
2. Skips fields that already have data (won't overwrite)
3. Commits all updates for a candidate at once
4. Logs success/failure for each field

### 4. Repeat

The agent processes candidates in batches. Run it multiple times to process all candidates:

```bash
# First run - processes first 10 candidates
python scripts/run_candidate_agent.py

# Second run - processes next 10 candidates
python scripts/run_candidate_agent.py

# Continue until all candidates are processed...
```

## Data Structure

The agent populates four types of data:

### Education Background

```json
{
    "graduation_year": 2000,
    "stream": "Political Science",
    "college_or_school": "Delhi University"
}
```

### Political Background

```json
{
    "elections": [
        {
            "election_year": 2019,
            "election_type": "MP",
            "constituency": "Delhi-1",
            "party": "Party Name",
            "status": "WON"
        }
    ]
}
```

### Family Background

```json
{
    "father": {
        "name": "Father Name",
        "profession": "Businessman"
    },
    "mother": {
        "name": "Mother Name",
        "profession": "Teacher"
    },
    "spouse": {
        "name": "Spouse Name",
        "profession": "Doctor"
    },
    "children": [
        {
            "name": "Child Name",
            "profession": "Engineer"
        }
    ]
}
```

### Assets

```json
{
    "commercial_assets": "2 shops, 1 hotel",
    "cash_assets": "Rs. 50 lakhs in bank",
    "bank_details": [
        {
            "bank_name": "State Bank of India",
            "branch": "Delhi Main"
        }
    ]
}
```

## Programmatic Usage

You can also use the agent in your own Python code:

```python
from app.database.session import get_db_session
from app.services.candidate_agent import CandidateDataAgent

# Initialize agent
agent = CandidateDataAgent(perplexity_api_key="your-key")

# Run with custom settings
with get_db_session() as session:
    stats = agent.run(
        session=session,
        batch_size=20,
        delay_between_candidates=2.0,
        delay_between_requests=2.0
    )

    print(f"Processed: {stats['total_processed']}")
    print(f"Successful: {stats['successful']}")
```

## Monitoring and Logging

The agent provides detailed logging:

```
2024-01-15 10:30:00 - INFO - Starting Candidate Data Population Agent
2024-01-15 10:30:00 - INFO - Found 10 candidates needing data
2024-01-15 10:30:01 - INFO - Processing candidate: Narendra Modi (ID: C001)
2024-01-15 10:30:02 - INFO - ✅ Education data found for Narendra Modi
2024-01-15 10:30:05 - INFO - ✅ Political history found for Narendra Modi
2024-01-15 10:30:08 - INFO - ✅ Family data found for Narendra Modi
2024-01-15 10:30:11 - INFO - ✅ Assets information found for Narendra Modi
2024-01-15 10:30:11 - INFO - ✅ Successfully updated Narendra Modi with 4 fields
```

## Error Handling

The agent handles various error scenarios:

### API Errors

If Perplexity API fails, the agent:

-   Logs the error
-   Continues with next candidate
-   Does not update the database for failed candidates

### Data Extraction Failures

If JSON extraction fails:

-   Logs a warning
-   Marks field as not populated
-   Continues with other fields

### Database Errors

If database update fails:

-   Rolls back the transaction
-   Logs the error
-   Continues with next candidate

## Best Practices

### 1. Start Small

Begin with small batch sizes to test:

```bash
python scripts/run_candidate_agent.py --batch-size 5
```

### 2. Monitor API Usage

Perplexity API has rate limits. Use appropriate delays:

```bash
# Conservative approach
python scripts/run_candidate_agent.py \
  --batch-size 10 \
  --delay-between-candidates 3.0 \
  --delay-between-requests 3.0
```

### 3. Run During Off-Peak Hours

For large batches, run during off-peak hours to avoid impacting other services.

### 4. Check Logs Regularly

Monitor the logs to ensure data quality and identify any issues.

### 5. Verify Data Quality

Periodically check the database to ensure the fetched data is accurate.

## Troubleshooting

### "No candidates found needing data"

All candidates already have complete data. The agent will exit gracefully.

### "Perplexity API key not provided"

Set the `PERPLEXITY_API_KEY` in your `.env` file or environment.

### "DATABASE_URL not set"

Set the `DATABASE_URL` in your `.env` file:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/rajniti
```

### Rate Limit Errors

Increase delays between requests:

```bash
python scripts/run_candidate_agent.py \
  --delay-between-candidates 5.0 \
  --delay-between-requests 5.0
```

### JSON Extraction Failures

This is normal - not all queries will return perfect JSON. The agent logs warnings and continues.

## Performance

Approximate processing times:

-   **Per Candidate**: 8-12 seconds (4 API calls with 2s delays)
-   **Batch of 10**: 2-3 minutes
-   **Batch of 100**: 20-30 minutes
-   **All 8,902 candidates**: ~20-30 hours (with delays)

To process all candidates faster, you can:

1. Run multiple instances in parallel (different batches)
2. Reduce delays (carefully, to avoid rate limits)
3. Increase batch size

## Future Enhancements

Potential improvements:

1. **Parallel Processing**: Process multiple candidates simultaneously
2. **Caching**: Cache Perplexity responses to avoid duplicate API calls
3. **Data Validation**: Add more sophisticated validation of fetched data
4. **Retry Logic**: Automatically retry failed API calls
5. **Priority Queue**: Process high-profile candidates first
6. **Scheduling**: Run agent on a schedule (cron job)

## Testing

Run the test suite:

```bash
# Run all agent tests
DATABASE_URL="sqlite:///test.db" pytest tests/test_candidate_agent.py -v

# Run specific test
DATABASE_URL="sqlite:///test.db" pytest tests/test_candidate_agent.py::test_agent_initialization -v
```

## Contributing

When modifying the agent:

1. Update tests in `tests/test_candidate_agent.py`
2. Update documentation
3. Test with small batch sizes first
4. Monitor logs for any issues
5. Run the full test suite

## Support

For issues or questions:

1. Check the logs for error details
2. Review the troubleshooting section
3. Open an issue on GitHub
