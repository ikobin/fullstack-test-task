from pathlib import Path
from typing import Protocol

from src.core.settings import Settings


class UploadedFile(Protocol):
    filename: str | None
    content_type: str | None

    async def read(self, size: int = -1) -> bytes: ...


class FileStorage:
    def __init__(self, settings: Settings) -> None:
        self._root = settings.storage_dir
        self._root.mkdir(parents=True, exist_ok=True)

    def path_for(self, stored_name: str) -> Path:
        stored_path = (self._root / stored_name).resolve()
        if not stored_path.is_relative_to(self._root.resolve()):
            raise ValueError("Invalid stored file name")
        return stored_path

    async def save_upload(self, stored_name: str, upload_file: UploadedFile) -> int:
        stored_path = self.path_for(stored_name)
        size = 0
        try:
            with stored_path.open("wb") as buffer:
                while chunk := await upload_file.read(64 * 1024):
                    size += len(chunk)
                    buffer.write(chunk)
        except Exception:
            stored_path.unlink(missing_ok=True)
            raise

        if size == 0:
            stored_path.unlink(missing_ok=True)
        return size

    def delete(self, stored_name: str) -> None:
        stored_path = self.path_for(stored_name)
        stored_path.unlink(missing_ok=True)

    def exists(self, stored_name: str) -> bool:
        return self.path_for(stored_name).exists()

    def read_text(self, stored_name: str) -> str:
        return self.path_for(stored_name).read_text(encoding="utf-8", errors="ignore")

    def read_bytes(self, stored_name: str) -> bytes:
        return self.path_for(stored_name).read_bytes()
