from typing import List, Dict, Optional, Any
import uuid
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton

logger = logging.getLogger(__name__)

class ChatHistoryService:
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()

    async def create_session(self, user_id: Optional[str] = None, title: str = "Nová konverzace") -> str:
        """Creates a new chat session and returns its ID."""
        try:
            data = {
                "title": title
            }
            if user_id:
                data["user_id"] = user_id
                
            response = self.supabase.table("chat_sessions").insert(data).execute()
            if response.data:
                return response.data[0]["id"]
            raise Exception("Failed to create session")
        except Exception as e:
            logger.error(f"Error creating chat session: {e}")
            # Fallback to a generated UUID if DB fails, though this won't persist
            return str(uuid.uuid4())

    async def add_message(self, session_id: str, role: str, content: str, citations: Optional[List[Dict]] = None):
        """Adds a message to a session."""
        try:
            data = {
                "session_id": session_id,
                "role": role,
                "content": content
            }
            if citations:
                data["citations"] = citations
                
            self.supabase.table("chat_messages").insert(data).execute()
        except Exception as e:
            logger.error(f"Error adding message to session {session_id}: {e}")

    async def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves all sessions for a user."""
        try:
            response = self.supabase.table("chat_sessions") \
                .select("*") \
                .eq("user_id", user_id) \
                .order("updated_at", desc=True) \
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching user sessions: {e}")
            return []

    async def get_session_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieves messages for a specific session."""
        try:
            response = self.supabase.table("chat_messages") \
                .select("*") \
                .eq("session_id", session_id) \
                .order("created_at", desc=False) \
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching session messages: {e}")
            return []
