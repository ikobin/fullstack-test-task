from fastapi import APIRouter, Depends

from src.api.deps import get_file_service
from src.schemas import AlertItem
from src.services.file_service import FileService

router = APIRouter()


@router.get("/alerts", response_model=list[AlertItem])
async def list_alerts_view(service: FileService = Depends(get_file_service)):
    return await service.list_alerts()
