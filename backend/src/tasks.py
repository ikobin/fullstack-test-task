from src.workers.celery_app import celery_app
from src.workers.tasks import scan_file_for_threats

celery_app.conf.imports = ("src.workers.tasks",)

__all__ = ["celery_app", "scan_file_for_threats"]
