import asyncio
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton
from backend.data_processing.embeddings.embedding_generator import EmbeddingGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_drug_embeddings():
    supabase = SupabaseSingleton.get_client()
    generator = EmbeddingGenerator()
    
    # 1. Fetch drugs without embeddings (or all if we want to refresh)
    # For now, let's fetch those with empty embedding. 
    # Note: postgres vector IS NULL check
    
    # Supabase-py doesn't easily support IS NULL filter in select without RPC or raw SQL?
    # We can fetch all and filter in python, or use a filter.
    # Actually .is_("embedding", "null") should work.
    
    logger.info("Fetching drugs without embeddings...")
    try:
        response = supabase.table("drugs").select("id, sukl_code, name, active_substance, spc_indications").is_("embedding", "null").execute()
        drugs = response.data
    except Exception as e:
        logger.error(f"Error fetching drugs: {e}")
        return

    total = len(drugs)
    logger.info(f"Found {total} drugs to process.")
    
    if total == 0:
        return

    batch_size = 50
    
    for i in range(0, total, batch_size):
        batch = drugs[i : i + batch_size]
        texts = []
        ids = []
        
        for drug in batch:
            # Create a text representation for embedding
            # "Name: ... Active Substance: ... SPC Indications: ..."
            text = f"Name: {drug.get('name', '')}. Active Substance: {drug.get('active_substance', '')}."
            if drug.get('spc_indications'):
                text += f" Indications: {drug.get('spc_indications')}"
                
            texts.append(text)
            ids.append(drug['id'])
            
        logger.info(f"Generating embeddings for batch {i//batch_size + 1}...")
        embeddings = generator.generate_embeddings(texts)
        
        if not embeddings:
            logger.warning("No embeddings generated for this batch.")
            continue
            
        # Update DB
        updates = []
        for j, emb in enumerate(embeddings):
            updates.append({
                "id": ids[j],
                "sukl_code": batch[j]["sukl_code"], # Include sukl_code to prevent NOT NULL violation if interpreted as insert
                "embedding": emb
            })
            
        try:
            # Explicitly specify on_conflict on primary key 'id' to ensure update
            supabase.table("drugs").upsert(updates, on_conflict="id").execute()
            logger.info(f"Updated {len(updates)} drugs with embeddings.")
        except Exception as e:
            logger.error(f"Error updating DB: {e}")

if __name__ == "__main__":
    asyncio.run(generate_drug_embeddings())
