from fastapi import APIRouter

api_router = APIRouter()
from backend.app.api.v1.endpoints import query
from backend.app.api.v1.endpoints import drugs
from backend.app.api.v1.endpoints import admin
from backend.app.api.v1.endpoints import ai

api_router.include_router(query.router, prefix="/query", tags=["query"])
api_router.include_router(drugs.router, prefix="/drugs", tags=["drugs"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
