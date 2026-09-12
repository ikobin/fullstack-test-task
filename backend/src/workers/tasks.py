import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.core.settings import get_settings
from src.repositories import AlertRepository, FileRepository
from src.services.processing import FileProcessingService
from src.services.storage import FileStorage
from src.workers.celery_app import celery_app


async def _process_uploaded_file(file_id: str) -> None:
    settings = get_settings()
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    storage = FileStorage(settings)
    try:
        async with session_maker() as session:
            service = FileProcessingService(
                files=FileRepository(session),
                alerts=AlertRepository(session),
                storage=storage,
            )
            await service.process(file_id)
    finally:
        await engine.dispose()


@celery_app.task(name="src.tasks.scan_file_for_threats")
def scan_file_for_threats(file_id: str) -> None:
    asyncio.run(_process_uploaded_file(file_id))
