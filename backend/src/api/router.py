from backend.src.api.routers.alerts import router as alerts_router
from backend.src.api.routers.files import router as files_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(files_router)
api_router.include_router(alerts_router)
