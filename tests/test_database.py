"""
Tests for database configuration.
"""
import os
from unittest.mock import MagicMock, patch

from app.core.database import check_db_health, init_db


class TestDatabaseConfiguration:
    """Test database configuration."""

    def test_init_db_without_url(self):
        """Test that database initialization handles missing DATABASE_URL."""
        with patch.dict(os.environ, {}, clear=True):
            result = init_db()
            assert result is False

    def test_init_db_with_invalid_url(self):
        """Test that database initialization handles invalid DATABASE_URL."""
        with patch.dict(
            os.environ,
            {"DATABASE_URL": "postgresql://invalid:invalid@localhost/invalid"},
        ):
            result = init_db()
            assert result is False

    def test_check_db_health_without_init(self):
        """Test database health check without initialization."""
        # Reset global engine
        import app.core.database as db_module

        original_engine = db_module.engine
        db_module.engine = None

        result = check_db_health()
        assert result is False

        # Restore original engine
        db_module.engine = original_engine

    @patch("app.core.database.create_engine")
    def test_init_db_success(self, mock_create_engine):
        """Test successful database initialization."""
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_create_engine.return_value = mock_engine

        with patch.dict(
            os.environ, {"DATABASE_URL": "postgresql://test:test@localhost/test"}
        ):
            result = init_db()
            assert result is True
            mock_create_engine.assert_called_once()
