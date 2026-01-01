from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.services.logger import get_logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from backend.services.cache import cache

from backend.app.api.v1.api import api_router
from backend.app.core.config import settings

# Load environment variables
load_dotenv()

# Initialize Logger
logger = get_logger(__name__)

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Backend service starting up")
    yield
    # Shutdown
    stats = cache.get_stats()
    logger.info("Backend service shutting down", cache_stats=stats)

app = FastAPI(
    title="Czech MedAI Backend",
    description="API for the Clinical AI Assistant",
    version="0.1.0",
    lifespan=lifespan
)

# Register Rate Limit Handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "ok", "service": "Czech MedAI Backend"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
