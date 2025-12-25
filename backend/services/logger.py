import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional

class StructuredLogger:
    """
    Logger that outputs logs in JSON format, suitable for cloud environments (AWS, Google Cloud, Docker).
    """
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Prevent adding multiple handlers if already exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = self.JsonFormatter()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            # Prevent propagation to root logger to avoid double logging
            self.logger.propagate = False

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            log_record = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "message": record.getMessage(),
                "logger_name": record.name,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }
            
            # Add extra fields if available
            if hasattr(record, "props") and isinstance(record.props, dict):
                log_record.update(record.props)
                
            # Add exception info if present
            if record.exc_info:
                log_record["exception"] = self.formatException(record.exc_info)
                
            return json.dumps(log_record)

    def info(self, message: str, **kwargs):
        self.logger.info(message, extra={"props": kwargs})

    def error(self, message: str, error: Optional[Exception] = None, **kwargs):
        if error:
            self.logger.error(f"{message}: {str(error)}", exc_info=error, extra={"props": kwargs})
        else:
            self.logger.error(message, extra={"props": kwargs})
            
        # Attempt to log to Supabase for errors (Fire and forget style)
        try:
           self._log_to_supabase("ERROR", message, error, **kwargs)
        except Exception:
           pass # Never break execution because of logging failure

    def warning(self, message: str, **kwargs):
        self.logger.warning(message, extra={"props": kwargs})

    def debug(self, message: str, **kwargs):
        self.logger.debug(message, extra={"props": kwargs})
        
    def _log_to_supabase(self, level: str, message: str, error: Optional[Exception] = None, **kwargs):
        # Local import to avoid circular dependency
        try:
            from backend.data_processing.utils.supabase_client import SupabaseSingleton
            client = SupabaseSingleton.get_client()
            
            payload = {
                "level": level,
                "message": message,
                "module": kwargs.get("module") or "unknown",
                "metadata": kwargs,
                "error_details": str(error) if error else None
            }
            
            # Note: In a real async app, this should be awaited or put in a background task. 
            # Since SupabaseSingleton uses sync client in some contexts, we need to be careful.
            # For this MVP python logging implementation, we will skip the DB write if explicitly async context is strictly required
            # or use the sync postgrest feature if available.
            # HOWEVER: The current implementation of SupabaseSingleton returns a client that *can* be used synchronously.
            
            client.table("app_errors").insert(payload).execute()
        except Exception:
            # Silent fail for now to avoid loops
            pass

# Global instance factory
def get_logger(name: str) -> StructuredLogger:
    return StructuredLogger(name)
