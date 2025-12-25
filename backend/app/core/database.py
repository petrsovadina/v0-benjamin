from supabase import create_client, Client
from backend.app.core.config import settings

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client instance using settings from config.
    """
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
