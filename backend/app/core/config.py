from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing import Self

class Settings(BaseSettings):
    PROJECT_NAME: str = "Czech MedAI"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"

    # CORS
    CORS_ORIGINS: list[str] = []

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # AI / LLM
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str | None = None
    
    # External APIs
    PUBMED_EMAIL: str
    
    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_ignore_empty=True, 
        extra="ignore"
    )
    
    @model_validator(mode='after')
    def validate_cors_origins_in_production(self) -> Self:
        """Validate that CORS_ORIGINS is not empty when ENVIRONMENT is production.
        
        This prevents a common security misconfiguration where production deployments
        may have no allowed CORS origins, effectively breaking frontend access.
        """
        if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
            raise ValueError(
                "CORS_ORIGINS must not be empty when ENVIRONMENT is 'production'. "
                "Please set CORS_ORIGINS environment variable with allowed origins, "
                "e.g., CORS_ORIGINS=[\"https://yourdomain.com\"]"
            )
        return self

settings = Settings()
