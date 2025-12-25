from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Czech MedAI"
    API_V1_STR: str = "/api/v1"
    
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

settings = Settings()
