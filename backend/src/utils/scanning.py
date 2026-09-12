from dataclasses import dataclass
from pathlib import Path

from src.models import StoredFile

SUSPICIOUS_EXTENSIONS = {".exe", ".bat", ".cmd", ".sh", ".js"}
LARGE_FILE_THRESHOLD_BYTES = 10 * 1024 * 1024
PDF_MIME_TYPES = {"application/pdf", "application/octet-stream"}


@dataclass(frozen=True)
class ScanResult:
    reasons: list[str]

    @property
    def is_suspicious(self) -> bool:
        return bool(self.reasons)

    @property
    def status(self) -> str:
        return "suspicious" if self.is_suspicious else "clean"

    @property
    def details(self) -> str:
        return ", ".join(self.reasons) if self.reasons else "no threats found"


def scan_file(file_item: StoredFile) -> ScanResult:
    reasons: list[str] = []
    extension = Path(file_item.original_name).suffix.lower()

    if extension in SUSPICIOUS_EXTENSIONS:
        reasons.append(f"suspicious extension {extension}")

    if file_item.size > LARGE_FILE_THRESHOLD_BYTES:
        reasons.append("file is larger than 10 MB")

    if extension == ".pdf" and file_item.mime_type not in PDF_MIME_TYPES:
        reasons.append("pdf extension does not match mime type")

    return ScanResult(reasons=reasons)
