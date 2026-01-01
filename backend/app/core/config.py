from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

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

    @model_validator(mode="after")
    def validate_production_cors(self) -> "Settings":
        """Validate that CORS_ORIGINS is not empty when ENVIRONMENT is production."""
        if self.ENVIRONMENT == "production" and not self.CORS_ORIGINS:
            raise ValueError(
                "CORS_ORIGINS must be explicitly configured when ENVIRONMENT is set to 'production'. "
                "Please set the CORS_ORIGINS environment variable with a JSON array of allowed origins, "
                "e.g., CORS_ORIGINS='[\"https://app.benjamin.cz\",\"https://benjamin.cz\"]'"
            )
        return self

settings = Settings()
