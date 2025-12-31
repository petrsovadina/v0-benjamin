from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "SuklDataPipeline"
    DEBUG: bool = False

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str  # Service role key preferred

    # OpenAI (for embeddings)
    OPENAI_API_KEY: str | None = None

    # Anthropic (for Agents)
    ANTHROPIC_API_KEY: str

    # Tools
    PUBMED_EMAIL: str | None = "admin@benjamin.cz"

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    RAW_DATA_DIR: Path = BASE_DIR / "raw_data"

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra env vars
    )

settings = Settings()
