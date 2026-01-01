from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

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
    def validate_cors_in_production(self) -> 'Settings':
        """Ensure CORS_ORIGINS is not empty in production environment."""
        if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
            raise ValueError(
                "CORS_ORIGINS must be explicitly configured (non-empty) when ENVIRONMENT is set to 'production'. "
                "This is required to prevent breaking the frontend in production."
            )
        return self

settings = Settings()
