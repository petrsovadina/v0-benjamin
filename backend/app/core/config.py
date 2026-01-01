from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
import logging

logger = logging.getLogger(__name__)

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
    def validate_production_cors(self) -> 'Settings':
        """Validate that CORS_ORIGINS is not empty in production environment."""
        if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
            logger.error(
                "CRITICAL: CORS_ORIGINS is empty in production environment. "
                "The frontend will not be able to connect to the API. "
                "Please set CORS_ORIGINS environment variable with allowed origins. "
                "Example: CORS_ORIGINS='[\"https://app.benjamin.cz\",\"https://benjamin.cz\"]'"
            )
            raise ValueError(
                "CORS_ORIGINS must not be empty when ENVIRONMENT is set to 'production'. "
                "Configure CORS_ORIGINS environment variable with a JSON array of allowed origins. "
                "Example: CORS_ORIGINS='[\"https://app.benjamin.cz\",\"https://benjamin.cz\"]'"
            )
        
        if self.ENVIRONMENT == "production" and self.CORS_ORIGINS:
            logger.info(f"Production CORS configured with {len(self.CORS_ORIGINS)} allowed origin(s)")
        
        return self

settings = Settings()
