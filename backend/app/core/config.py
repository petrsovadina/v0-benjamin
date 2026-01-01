from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

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
    
    @field_validator('CORS_ORIGINS')
    @classmethod
    def validate_cors_origins_in_production(cls, v, info):
        """Ensure CORS_ORIGINS is not empty when ENVIRONMENT is production."""
        # Access other field values via info.data
        environment = info.data.get('ENVIRONMENT', 'development')
        if environment == 'production' and not v:
            raise ValueError(
                'CORS_ORIGINS must not be empty when ENVIRONMENT is set to "production". '
                'Please configure allowed origins in your environment variables.'
            )
        return v
    
    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_ignore_empty=True, 
        extra="ignore"
    )

settings = Settings()
