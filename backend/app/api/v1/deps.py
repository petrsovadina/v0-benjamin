from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.database import get_supabase_client
from backend.app.core.config import settings
from typing import Optional, Dict, Any
from supabase.client import Client

security = HTTPBearer()

async def get_current_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return credentials.credentials

async def get_current_user(token: str = Depends(get_current_user_token)) -> Dict[str, Any]:
    """
    Validates the token with Supabase Auth and returns the User object.
    Also ensures the user exists in 'public.users'.
    """
    supabase = get_supabase_client()
    
    try:
        # 1. Validate Token and Get Auth User
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        auth_user = user_response.user
        
        # 2. Sync with public.users
        # Check if user exists
        res = supabase.table("users").select("*").eq("auth_id", auth_user.id).execute()
        
        if not res.data:
            # First time login - Create user record
            # Extract metadata
            metadata = auth_user.user_metadata or {}
            first_name = metadata.get("first_name", "Unknown")
            last_name = metadata.get("last_name", "User")
            
            new_user = {
                "auth_id": auth_user.id,
                "email": auth_user.email,
                "first_name": first_name,
                "last_name": last_name,
                "role": "physician" # Default
            }
            
            # Insert and get Query Response
            insert_res = supabase.table("users").insert(new_user).execute()
            if insert_res.data:
                return insert_res.data[0]
            else:
                 raise HTTPException(status_code=500, detail="Failed to create user profile")
        
        return res.data[0]
        
    except Exception as e:
        # If it's already an HTTPException, re-raise
        if isinstance(e, HTTPException):
            raise e
        print(f"Auth Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
