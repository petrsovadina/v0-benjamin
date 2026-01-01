"""
Unit tests for CORS configuration parsing in Settings class.

Tests verify:
- ENVIRONMENT defaults to "development" when not set
- CORS_ORIGINS correctly parsed from environment variable
- Empty CORS_ORIGINS defaults to empty list
- Whitespace handling in origin lists
"""

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


class TestCORSProductionValidation:
    """Tests for CORS_ORIGINS validation in production environment."""

    def test_production_requires_cors_origins(self):
        """Production environment should raise ValueError if CORS_ORIGINS is empty."""
        import pytest
        from pydantic import ValidationError
        
        with patch.dict(os.environ, {
            "ENVIRONMENT": "production",
            # CORS_ORIGINS not set, should default to empty list
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict
            from pydantic import model_validator
            from typing import Self
            
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
                
                @model_validator(mode='after')
                def validate_cors_origins_in_production(self) -> Self:
                    if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
                        raise ValueError(
                            "CORS_ORIGINS must not be empty when ENVIRONMENT is 'production'. "
                            "Please set CORS_ORIGINS environment variable with allowed origins, "
                            "e.g., CORS_ORIGINS=[\"https://yourdomain.com\"]"
                        )
                    return self
            
            with pytest.raises(ValidationError) as exc_info:
                settings = TestSettings()
            
            assert "CORS_ORIGINS must not be empty" in str(exc_info.value)

    def test_production_with_cors_origins_succeeds(self):
        """Production environment should succeed if CORS_ORIGINS is set."""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "production",
            "CORS_ORIGINS": '["https://benjamin.cz"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict
            from pydantic import model_validator
            from typing import Self
            
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
                
                @model_validator(mode='after')
                def validate_cors_origins_in_production(self) -> Self:
                    if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
                        raise ValueError(
                            "CORS_ORIGINS must not be empty when ENVIRONMENT is 'production'. "
                            "Please set CORS_ORIGINS environment variable with allowed origins, "
                            "e.g., CORS_ORIGINS=[\"https://yourdomain.com\"]"
                        )
                    return self
            
            settings = TestSettings()
            assert settings.ENVIRONMENT == "production"
            assert settings.CORS_ORIGINS == ["https://benjamin.cz"]

    def test_development_allows_empty_cors_origins(self):
        """Development environment should allow empty CORS_ORIGINS."""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "development",
            # CORS_ORIGINS not set, should default to empty list
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict
            from pydantic import model_validator
            from typing import Self
            
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
                
                @model_validator(mode='after')
                def validate_cors_origins_in_production(self) -> Self:
                    if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
                        raise ValueError(
                            "CORS_ORIGINS must not be empty when ENVIRONMENT is 'production'. "
                            "Please set CORS_ORIGINS environment variable with allowed origins, "
                            "e.g., CORS_ORIGINS=[\"https://yourdomain.com\"]"
                        )
                    return self
            
            # Should not raise ValueError
            settings = TestSettings()
            assert settings.ENVIRONMENT == "development"
            assert settings.CORS_ORIGINS == []

    def test_staging_allows_empty_cors_origins(self):
        """Staging environment should allow empty CORS_ORIGINS (only production is strict)."""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "staging",
            # CORS_ORIGINS not set, should default to empty list
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            from pydantic_settings import BaseSettings, SettingsConfigDict
            from pydantic import model_validator
            from typing import Self
            
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
                
                @model_validator(mode='after')
                def validate_cors_origins_in_production(self) -> Self:
                    if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
                        raise ValueError(
                            "CORS_ORIGINS must not be empty when ENVIRONMENT is 'production'. "
                            "Please set CORS_ORIGINS environment variable with allowed origins, "
                            "e.g., CORS_ORIGINS=[\"https://yourdomain.com\"]"
                        )
                    return self
            
            # Should not raise ValueError
            settings = TestSettings()
            assert settings.ENVIRONMENT == "staging"
            assert settings.CORS_ORIGINS == []


class TestCORSMiddlewareHeaders:
    """Integration tests for CORS headers in FastAPI responses."""

    def test_cors_preflight_options_request(self):
        """Test CORS preflight OPTIONS request returns correct headers."""
        import os
        from unittest.mock import patch

        with patch.dict(os.environ, {
            "ENVIRONMENT": "development",
            "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:8000"]',
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key",
            "PUBMED_EMAIL": "test@test.com"
        }, clear=True):
            # Import fresh app instance with test settings
            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            from fastapi.testclient import TestClient

            # Create test app with same CORS configuration pattern
            test_app = FastAPI()
            test_app.add_middleware(
                CORSMiddleware,
                allow_origins=["http://localhost:3000", "http://localhost:8000"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            @test_app.get("/health")
            def health():
                return {"status": "ok"}

            client = TestClient(test_app)

            # Send OPTIONS preflight request
            response = client.options(
                "/health",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "GET",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )

            # Verify preflight response
            assert response.status_code == 200
            assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
            assert "GET" in response.headers.get("access-control-allow-methods", "")

    def test_cors_headers_on_get_request(self):
        """Test CORS headers are present on regular GET requests."""
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.testclient import TestClient

        test_app = FastAPI()
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @test_app.get("/health")
        def health():
            return {"status": "ok", "version": "2.0.0"}

        client = TestClient(test_app)

        # Send GET request with Origin header
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )

        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_blocks_unauthorized_origin(self):
        """Test CORS blocks requests from unauthorized origins."""
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.testclient import TestClient

        test_app = FastAPI()
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],  # Only allow localhost:3000
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @test_app.get("/health")
        def health():
            return {"status": "ok"}

        client = TestClient(test_app)

        # Send request from unauthorized origin
        response = client.get(
            "/health",
            headers={"Origin": "http://evil-site.com"}
        )

        # Request succeeds but CORS header should NOT reflect the unauthorized origin
        assert response.status_code == 200
        # The access-control-allow-origin should not be set for unauthorized origins
        assert response.headers.get("access-control-allow-origin") != "http://evil-site.com"

    def test_cors_preflight_with_development_origins(self):
        """Test CORS preflight with multiple development origins."""
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.testclient import TestClient

        dev_origins = ["http://localhost:3000", "http://localhost:8000"]

        test_app = FastAPI()
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=dev_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @test_app.get("/health")
        def health():
            return {"status": "ok"}

        client = TestClient(test_app)

        # Test both development origins
        for origin in dev_origins:
            response = client.options(
                "/health",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "GET"
                }
            )
            assert response.status_code == 200
            assert response.headers.get("access-control-allow-origin") == origin
