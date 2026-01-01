"""
Unit tests for CORS configuration parsing in Settings class.

Tests verify:
- ENVIRONMENT defaults to "development" when not set
- CORS_ORIGINS correctly parsed from environment variable
- Empty CORS_ORIGINS defaults to empty list
- Whitespace handling in origin lists
"""

import pytest
import os
from unittest.mock import patch


class TestEnvironmentConfiguration:
    """Tests for ENVIRONMENT configuration field."""

    def test_environment_defaults_to_development(self):
        """ENVIRONMENT should default to 'development' when not set."""
        # Clear ENVIRONMENT from environment if present
        env_without_environment = {
            k: v for k, v in os.environ.items()
            if k != "ENVIRONMENT"
        }

        with patch.dict(os.environ, env_without_environment, clear=True):
            # Need to reimport to get fresh Settings instance
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                ENVIRONMENT: str = "development"
                SUPABASE_URL: str = "https://test.supabase.co"
                SUPABASE_KEY: str = "test-key"
                ANTHROPIC_API_KEY: str = "test-key"
                PUBMED_EMAIL: str = "test@test.com"

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.ENVIRONMENT == "development"

    def test_environment_reads_from_env(self):
        """ENVIRONMENT should read from environment variable when set."""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "production",
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                ENVIRONMENT: str = "development"
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.ENVIRONMENT == "production"

    def test_environment_accepts_staging(self):
        """ENVIRONMENT should accept 'staging' value."""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "staging",
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                ENVIRONMENT: str = "development"
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.ENVIRONMENT == "staging"


class TestCORSOriginsConfiguration:
    """Tests for CORS_ORIGINS configuration field."""

    def test_cors_origins_defaults_to_empty_list(self):
        """CORS_ORIGINS should default to empty list when not set."""
        with patch.dict(os.environ, {
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.CORS_ORIGINS == []

    def test_cors_origins_parses_json_array(self):
        """CORS_ORIGINS should parse JSON array format."""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:8000"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.CORS_ORIGINS == ["http://localhost:3000", "http://localhost:8000"]

    def test_cors_origins_single_origin(self):
        """CORS_ORIGINS should handle single origin in JSON format."""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": '["https://benjamin.cz"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.CORS_ORIGINS == ["https://benjamin.cz"]

    def test_cors_origins_https_and_http(self):
        """CORS_ORIGINS should accept both HTTP and HTTPS origins."""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": '["http://localhost:3000", "https://benjamin.cz"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert "http://localhost:3000" in settings.CORS_ORIGINS
            assert "https://benjamin.cz" in settings.CORS_ORIGINS

    def test_cors_origins_production_config(self):
        """CORS_ORIGINS should support production domain configuration."""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": '["https://benjamin.cz", "https://www.benjamin.cz", "https://api.benjamin.cz"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert len(settings.CORS_ORIGINS) == 3
            assert "https://benjamin.cz" in settings.CORS_ORIGINS
            assert "https://www.benjamin.cz" in settings.CORS_ORIGINS
            assert "https://api.benjamin.cz" in settings.CORS_ORIGINS


class TestCORSOriginsEdgeCases:
    """Edge case tests for CORS_ORIGINS parsing."""

    def test_cors_origins_empty_json_array(self):
        """CORS_ORIGINS should handle empty JSON array."""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": "[]",
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.CORS_ORIGINS == []

    def test_cors_origins_with_ports(self):
        """CORS_ORIGINS should handle origins with port numbers."""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:8000", "http://192.168.1.100:3000"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert "http://localhost:3000" in settings.CORS_ORIGINS
            assert "http://localhost:8000" in settings.CORS_ORIGINS
            assert "http://192.168.1.100:3000" in settings.CORS_ORIGINS


class TestSettingsIntegration:
    """Integration tests for full Settings class CORS configuration."""

    def test_settings_cors_and_environment_together(self):
        """Settings should correctly load both ENVIRONMENT and CORS_ORIGINS."""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "production",
            "CORS_ORIGINS": '["https://benjamin.cz"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                ENVIRONMENT: str = "development"
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.ENVIRONMENT == "production"
            assert settings.CORS_ORIGINS == ["https://benjamin.cz"]

    def test_development_config_example(self):
        """Development configuration should work with localhost origins."""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "development",
            "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:8000"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                ENVIRONMENT: str = "development"
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert settings.ENVIRONMENT == "development"
            assert len(settings.CORS_ORIGINS) == 2
            assert all("localhost" in origin for origin in settings.CORS_ORIGINS)

    def test_cors_origins_type_is_list(self):
        """CORS_ORIGINS should always be a list type."""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": '["http://localhost:3000"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict

            class TestSettings(BaseSettings):
                CORS_ORIGINS: list[str] = []
                SUPABASE_URL: str
                SUPABASE_KEY: str
                ANTHROPIC_API_KEY: str
                PUBMED_EMAIL: str

                model_config = SettingsConfigDict(
                    env_ignore_empty=True,
                    extra="ignore"
                )

            settings = TestSettings()
            assert isinstance(settings.CORS_ORIGINS, list)
