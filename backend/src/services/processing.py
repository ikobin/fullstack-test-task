from backend.src.utils.metadata import extract_metadata
from backend.src.utils.scanning import scan_file

from src.models import Alert, StoredFile
from src.repositories import AlertRepository, FileRepository
from src.services.storage import FileStorage


class FileProcessingService:
    def __init__(
        self,
        files: FileRepository,
        alerts: AlertRepository,
        storage: FileStorage,
    ) -> None:
        self._files = files
        self._alerts = alerts
        self._storage = storage

    async def process(self, file_id: str) -> None:
        file_item = await self._files.get(file_id)
        if not file_item:
            return

        await self._apply_scan(file_item)
        await self._apply_metadata(file_item)
        await self._send_alert(file_item)

    async def _apply_scan(self, file_item: StoredFile) -> None:
        file_item.processing_status = "processing"
        result = scan_file(file_item)
        file_item.scan_status = result.status
        file_item.scan_details = result.details
        file_item.requires_attention = result.is_suspicious
        await self._files.save(file_item)

    async def _apply_metadata(self, file_item: StoredFile) -> None:
        if not self._storage.exists(file_item.stored_name):
            file_item.processing_status = "failed"
            file_item.scan_status = file_item.scan_status or "failed"
            file_item.scan_details = "stored file not found during metadata extraction"
            await self._files.save(file_item)
            return

        file_item.metadata_json = extract_metadata(file_item, self._storage)
        file_item.processing_status = "processed"
        await self._files.save(file_item)

    async def _send_alert(self, file_item: StoredFile) -> None:
        if file_item.processing_status == "failed":
            alert = Alert(file_id=file_item.id, level="critical", message="File processing failed")
        elif file_item.requires_attention:
            alert = Alert(
                file_id=file_item.id,
                level="warning",
                message=f"File requires attention: {file_item.scan_details}",
            )
        else:
            alert = Alert(file_id=file_item.id, level="info", message="File processed successfully")

        await self._alerts.add(alert)
