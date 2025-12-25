from supabase import create_client, Client
from backend.data_processing.config.settings import settings

class SupabaseSingleton:
    _instance = None
    client: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls.client is None:
            cls.client = create_client(
                settings.SUPABASE_URL, 
                settings.SUPABASE_KEY
            )
        return cls.client
