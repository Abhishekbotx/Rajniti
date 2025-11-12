"""
Database configuration module.

Supports both local PostgreSQL and Supabase (PostgreSQL-based).
"""

import os
from typing import Optional


def get_database_url() -> str:
    """
    Get database URL from environment variables.
    
    Supports both local PostgreSQL and Supabase.
    
    Environment variables (in priority order):
    - DATABASE_URL: Full database connection string
    - SUPABASE_DB_URL: Supabase database connection string
    - Individual components: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    
    Returns:
        Database URL string compatible with SQLAlchemy
    
    Examples:
        Local: postgresql://user:password@localhost:5432/rajniti
        Supabase: postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
    """
    # First check for direct DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    
    # Check for Supabase database URL
    supabase_db_url = os.getenv("SUPABASE_DB_URL")
    if supabase_db_url:
        return supabase_db_url
    
    # Build from individual components
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "rajniti")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_echo_mode() -> bool:
    """
    Get SQLAlchemy echo mode from environment.
    
    Returns:
        True if SQL queries should be logged, False otherwise
    """
    return os.getenv("DB_ECHO", "false").lower() == "true"
