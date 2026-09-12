import mimetypes
from pathlib import Path
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import EmptyFileError, NotFoundError
from src.models import Alert, StoredFile
from src.repositories import AlertRepository, FileRepository
from src.services.storage import FileStorage, UploadedFile


class FileService:
    def __init__(self, session: AsyncSession, storage: FileStorage) -> None:
        self._files = FileRepository(session)
        self._alerts = AlertRepository(session)
        self._storage = storage

    async def list_files(self) -> list[StoredFile]:
        return await self._files.list_all()

    async def list_alerts(self) -> list[Alert]:
        return await self._alerts.list_all()

    async def get_file(self, file_id: str) -> StoredFile:
        file_item = await self._files.get(file_id)
        if file_item is None:
            raise NotFoundError("File not found")
        return file_item

    async def create_file(self, title: str, upload_file: UploadedFile) -> StoredFile:
        file_id = str(uuid4())
        suffix = Path(upload_file.filename or "").suffix
        stored_name = f"{file_id}{suffix}"
        size = await self._storage.save_upload(stored_name, upload_file)
        if size == 0:
            raise EmptyFileError("File is empty")

        file_item = StoredFile(
            id=file_id,
            title=title,
            original_name=upload_file.filename or stored_name,
            stored_name=stored_name,
            mime_type=upload_file.content_type
            or mimetypes.guess_type(stored_name)[0]
            or "application/octet-stream",
            size=size,
            processing_status="uploaded",
        )
        try:
            return await self._files.add(file_item)
        except Exception:
            self._storage.delete(stored_name)
            raise

    async def update_file(self, file_id: str, title: str) -> StoredFile:
        file_item = await self.get_file(file_id)
        file_item.title = title
        return await self._files.save(file_item)

    async def delete_file(self, file_id: str) -> None:
        file_item = await self.get_file(file_id)
        stored_name = file_item.stored_name
        await self._files.delete(file_item)
        self._storage.delete(stored_name)

    async def get_download(self, file_id: str) -> tuple[StoredFile, Path]:
        file_item = await self.get_file(file_id)
        if not self._storage.exists(file_item.stored_name):
            raise NotFoundError("Stored file not found")
        return file_item, self._storage.path_for(file_item.stored_name)
