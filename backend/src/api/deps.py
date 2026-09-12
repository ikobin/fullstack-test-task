from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import Settings, get_settings
from src.db import get_session
from src.services.file_service import FileService
from src.services.storage import FileStorage


def get_settings_dep() -> Settings:
    return get_settings()


def get_file_service(
    session: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings_dep),
) -> FileService:
    return FileService(session=session, storage=FileStorage(settings))
