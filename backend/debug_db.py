from supabase import create_client
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env explicitly
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

query = "algifen"
print(f"Testing search for '{query}'...")

try:
    # Exact match test
    response = supabase.table("drugs").select("*").eq("name_normalized", query).execute()
    print(f"Exact match found: {len(response.data)}")
    
    # ILIKE test
    response = supabase.table("drugs").select("*").ilike("name_normalized", f"%{query}%").execute()
    print(f"ILIKE match found: {len(response.data)}")

    # Check the actual value
    response = supabase.table("drugs").select("name_normalized").eq("sukl_code", "0000001").execute()
    if response.data:
        actual_val = response.data[0]['name_normalized']
        print(f"Actual value in DB for 0000001: '{actual_val}' (len: {len(actual_val)})")
        print(f"Query value: '{query}' (len: {len(query)})")
        print(f"Match? {actual_val == query}")
    
except Exception as e:
    print(f"Error: {e}")
