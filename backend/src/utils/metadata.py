from pathlib import Path

from src.models import StoredFile
from src.services.storage import FileStorage


def extract_metadata(file_item: StoredFile, storage: FileStorage) -> dict:
    metadata = {
        "extension": Path(file_item.original_name).suffix.lower(),
        "size_bytes": file_item.size,
        "mime_type": file_item.mime_type,
    }

    if file_item.mime_type.startswith("text/"):
        content = storage.read_text(file_item.stored_name)
        metadata["line_count"] = len(content.splitlines())
        metadata["char_count"] = len(content)
    elif file_item.mime_type == "application/pdf":
        content = storage.read_bytes(file_item.stored_name)
        metadata["approx_page_count"] = max(content.count(b"/Type /Page"), 1)

    return metadata
