from fastapi import APIRouter
from core.config import settings
from modules.auth.routes import router as auth_routes
from modules.storage.routes import router as storage_routes

api_router = APIRouter(prefix=settings.API_V1_PREFIX)

api_router.include_router(auth_routes, prefix="/auth", tags=["auth"])
api_router.include_router(storage_routes, prefix="/namenode", tags=["namenode"])
