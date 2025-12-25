import argparse
import asyncio
import logging
from pathlib import Path

from backend.data_processing.config.settings import settings

# Imports from new structure
from backend.data_processing.parsers.sukl_dlp_parser import SuklDlpParser
from backend.data_processing.loaders.drug_loader import DrugLoader

from backend.data_processing.parsers.sukl_pricing_parser import SuklPricingParser
from backend.data_processing.loaders.pricing_loader import PricingLoader

from backend.data_processing.parsers.spc_pil_parser import SpcPilParser
from backend.data_processing.loaders.document_loader import DocumentLoader
from backend.data_processing.embeddings.embedding_generator import EmbeddingGenerator
from backend.data_processing.downloaders.sukl_downloader import SuklDownloader

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    parser = argparse.ArgumentParser(description="run_pipeline")
    parser.add_argument("--download", action="store_true", help="Download raw CSVs")
    parser.add_argument("--drugs", action="store_true", help="Run Drug pipeline (DLP)")
    parser.add_argument("--pricing", action="store_true", help="Run Pricing pipeline")
    parser.add_argument("--embeddings", action="store_true", help="Process embeddings (separate mode, not yet implemented)")
    parser.add_argument("--with-embeddings", action="store_true", help="Enable vector embedding generation during drug processing")
    parser.add_argument("--documents", action="store_true", help="Generate SPC/PIL metadata")
    parser.add_argument("--guidelines", action="store_true", help="Run Guidelines Ingestion (PDFs)")
    parser.add_argument("--substances", action="store_true", help="Run Active Substances pipeline")
    parser.add_argument("--limit", type=int, default=None, help="Limit items processed")
    parser.add_argument("--all", action="store_true", help="Run full pipeline")
    
    args = parser.parse_args()

    # Paths (using settings)
    raw_data_path = settings.RAW_DATA_DIR
    dlp_path = raw_data_path / "dlp_leciva.csv"
    pricing_path = raw_data_path / "scau_leciva.csv"
    substances_path = raw_data_path / "nkod_dlp_lecivelatky.csv"

    # Default to all if no specific flag
    if args.all or (not args.download and not args.drugs and not args.pricing and not args.documents and not args.guidelines and not args.substances):
        args.download = True
        args.drugs = True
        args.pricing = True
        args.documents = True
        args.guidelines = True
        args.substances = True

    if args.download:
        logger.info("--- Downloading Data ---")
        downloader = SuklDownloader()
        await downloader.download_all()

        # 2b. Download Documents Mapping & Auxiliary Files
        await downloader.download_with_retry("dlp_monthly", "dlp_nazvydokumentu.csv", file_pattern="nazvydokumentu")
        await downloader.download_with_retry("dlp_monthly", "dlp_atc.csv", file_pattern="dlp_atc.csv")
        await downloader.download_with_retry("dlp_monthly", "dlp_latky.csv", file_pattern="dlp_latky.csv")

    if args.substances:
         logger.info("--- Running Active Substances Pipeline ---")
         if not substances_path.exists():
             logger.warning(f"Active substances file {substances_path} not found. Skipping.")
         else:
             from backend.data_processing.parsers.active_substance_parser import ActiveSubstanceParser
             from backend.data_processing.loaders.active_substance_loader import ActiveSubstanceLoader
             
             parser = ActiveSubstanceParser(str(substances_path))
             items = parser.parse(limit=args.limit)
             loader = ActiveSubstanceLoader()
             loader.load_substances(items)

    if args.drugs:
        logger.info("--- Running Drug Pipeline ---")
        # Initialize EmbeddingGenerator for search text creation (and embeddings if key present)
        from backend.data_processing.generators.embedding_generator import EmbeddingGenerator
        emb_gen = EmbeddingGenerator()
        should_embed = args.with_embeddings and settings.OPENAI_API_KEY

        if args.with_embeddings and not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set. Skipping embedding generation despite --with-embeddings flag.")
        
        from backend.data_processing.parsers.auxiliary_parser import AuxiliaryParser
        
        # 1. Load Auxiliary Maps (ATC, Active Substances)
        atc_path = raw_data_path / "dlp_atc.csv"
        dlp_latky_path = raw_data_path / "dlp_latky.csv"

        aux_parser = AuxiliaryParser()
        atc_map = {}
        if atc_path.exists():
            logger.info(f"Loading ATC map from {atc_path}")
            atc_map = aux_parser.parse_atc(str(atc_path))
        else:
            logger.warning(f"ATC file {atc_path} not found. ATC names will not be mapped.")

        active_substance_map = {}
        if dlp_latky_path.exists():
            logger.info(f"Loading Active Substances map from {dlp_latky_path}")
            active_substance_map = aux_parser.parse_substances(str(dlp_latky_path))
        else:
            logger.warning(f"DLP Latky file {dlp_latky_path} not found. Active substances will not be mapped.")

        drug_loader = DrugLoader()
        
        # Process Monthly DLP
        if dlp_path.exists():
            logger.info(f"Processing Monthly DLP: {dlp_path}")
            parser = SuklDlpParser(str(dlp_path))
            items = parser.parse(limit=args.limit)
            
            # Enrich and load in batches
            batch_size = 100
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                
                # Enrich with ATC names and active substances
                for item in batch:
                    item['atc_name'] = atc_map.get(item.get('atc_code'), "")
                    # active_substances from map? or raw? current parser gets generic list?
                    # Auxiliary map returns list of dicts. We need mapping by CODE? 
                    # Sukl parser has 'sukl_code'. Does latky have sukl_code?
                    # dlp_latky has KOD_LATKY. Mapping KOD_SUKL -> KOD_LATKY is in dlp_slozeni.csv?
                    # The user guide said "Auxiliary Data: Ingest dlp_atc.csv, dlp_latky.csv".
                    # Direct mapping might be tricky without dlp_slozeni.
                    # For now I will proceed with just ATC mapping and generating search text from existing item fields.
                    
                    item['search_text'] = emb_gen.create_search_text(item, item['atc_name'])

                # Generate embeddings for the batch if enabled
                if should_embed:
                    texts_to_embed = [item['search_text'] for item in batch if item.get('search_text')]
                    if texts_to_embed:
                        try:
                            embeddings = emb_gen.generate_embeddings(texts_to_embed)
                            for j, item in enumerate(batch):
                                if item.get('search_text'):
                                    item['embedding'] = embeddings[j]
                        except Exception as e:
                            logger.error(f"Embedding failed for batch {i}: {e}")
                    else:
                        logger.warning(f"No search text to embed for batch starting at index {i}.")

                # Load the batch
                drug_loader.load_drugs(batch)
                logger.info(f"Processed and loaded {min(batch_size, len(items) - i)} drugs (Monthly DLP).")
        else:
             logger.warning(f"Monthly DLP file not found at {dlp_path}")

        # Process Current DLP (eRecept) - Upsert to get latest state
        erecept_path = raw_data_path / "dlp_erecept.csv"
        if erecept_path.exists():
            logger.info(f"Processing Current DLP (eRecept): {erecept_path}")
            parser = SuklDlpParser(str(erecept_path))
            items = parser.parse(limit=args.limit)

            # Enrich and load in batches
            batch_size = 100
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                
                # Enrich with ATC names and active substances
                for item in batch:
                    item['atc_name'] = atc_map.get(item.get('atc_code'), "")
                    # Same logic for active substances - simplified for now
                    
                    item['search_text'] = emb_gen.create_search_text(item, item['atc_name'])

                # Generate embeddings for the batch if enabled
                if should_embed:
                    texts_to_embed = [item['search_text'] for item in batch if item.get('search_text')]
                    if texts_to_embed:
                        try:
                            embeddings = emb_gen.generate_embeddings(texts_to_embed)
                            for j, item in enumerate(batch):
                                if item.get('search_text'):
                                    item['embedding'] = embeddings[j]
                        except Exception as e:
                            logger.error(f"Embedding failed for eRecept batch {i}: {e}")
                    else:
                        logger.warning(f"No search text to embed for eRecept batch starting at index {i}.")

                # Load the batch
                drug_loader.load_drugs(batch)
                logger.info(f"Processed and loaded {min(batch_size, len(items) - i)} drugs (eRecept DLP).")
        else:
             logger.info(f"Current DLP file not found at {erecept_path}")

    if args.pricing:
        logger.info("--- Running Pricing Pipeline ---")
        
        # 1. Current Pricing (Update Drugs table)
        if pricing_path.exists():
            logger.info(f"Processing Current Pricing: {pricing_path}")
            parser = SuklPricingParser()
            items = parser.parse_pricing(pricing_path)
            if args.limit:
                items = items[:args.limit]
            loader = PricingLoader()
            loader.load_pricing(items)
        else:
            logger.warning(f"Pricing file {pricing_path} not found. Skipping.")

        # 2. Historical Pricing (Archives)
        # Assuming we want to process archives if they exist, or via flag?
        # Let's stick to explicit flag --archives or just checking file existence if user downloaded them
        # Implementation: Check for 2024, 2023 zips
        
        archives = [
            raw_data_path / "lek13_2024.zip",
            raw_data_path / "lek13_2023.zip",
            raw_data_path / "lek13_2025_10.csv"
        ]
        
        # Only process if present
        found_archives = [p for p in archives if p.exists()]
        
        if found_archives:
            logger.info(f"Found {len(found_archives)} archives/historical files. Processing...")
            from backend.data_processing.loaders.price_history_loader import PriceHistoryLoader
            
            history_loader = PriceHistoryLoader()
            parser = SuklPricingParser()
            
            for arch_path in found_archives:
                logger.info(f"Parsing archive: {arch_path}")
                history_items = parser.parse_pricing(arch_path)
                
                if args.limit:
                    history_items = history_items[:args.limit]
                
                history_loader.load_price_history(history_items)
        else:
            logger.info("No pricing archives found. Use --download to fetch them if needed.")

    if args.documents:
        logger.info("--- Running Documents Mapping Pipeline ---")
        
        # 1. Parse Mapping
        mapping_file = raw_data_path / "dlp_nazvydokumentu.csv"
        if mapping_file.exists():
            from backend.data_processing.parsers.sukl_document_parser import SuklDocumentParser
            from backend.data_processing.loaders.document_mapping_loader import DocumentMappingLoader
            
            parser = SuklDocumentParser()
            items = parser.parse_mapping(mapping_file)
            
            if args.limit:
                items = items[:args.limit]
                
            loader = DocumentMappingLoader()
            loader.load_mapping(items)
        else:
            logger.warning(f"Document mapping file {mapping_file} not found. Run --download.")

    if args.guidelines:
        logger.info("--- Running Guidelines Pipeline ---")
        from backend.data_processing.loaders.guidelines_loader import GuidelinesLoader
        loader = GuidelinesLoader()
        await loader.ingest_pdfs()

if __name__ == "__main__":
    asyncio.run(main())
