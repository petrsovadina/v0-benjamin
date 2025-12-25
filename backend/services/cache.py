import time
from typing import Any, Dict, Optional, Tuple

class SimpleCache:
    """
    A simple in-memory cache with TTL (Time To Live).
    """
    def __init__(self):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache. Returns None if key not found or expired.
        """
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                self._hits += 1
                return value
            else:
                try:
                    del self._cache[key]
                except KeyError:
                    pass
        
        self._misses += 1
        return None

    def set(self, key: str, value: Any, ttl: int = 300):
        """
        Set a value in the cache with a TTL (default 5 minutes).
        """
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)

    def clear(self):
        """
        Clear all cache entries.
        """
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """
        Returns cache statistics.
        """
        total = self._hits + self._misses
        hit_rate = (self._hits / total) if total > 0 else 0.0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "total_requests": total,
            "hit_rate": round(hit_rate, 2),
            "size": len(self._cache)
        }

# Global instance
cache = SimpleCache()
