from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse
from starlette import status

from src.api.deps import get_file_service
from src.schemas import FileItem, FileUpdate
from src.services.file_service import FileService
from src.workers.tasks import scan_file_for_threats

router = APIRouter()


@router.get("/files", response_model=list[FileItem])
async def list_files_view(service: FileService = Depends(get_file_service)):
    return await service.list_files()


@router.post("/files", response_model=FileItem, status_code=201)
async def create_file_view(
    title: str = Form(...),
    file: UploadFile = File(...),
    service: FileService = Depends(get_file_service),
):
    file_item = await service.create_file(title=title, upload_file=file)
    scan_file_for_threats.delay(file_item.id)
    return file_item


@router.get("/files/{file_id}", response_model=FileItem)
async def get_file_view(file_id: str, service: FileService = Depends(get_file_service)):
    return await service.get_file(file_id)


@router.patch("/files/{file_id}", response_model=FileItem)
async def update_file_view(
    file_id: str,
    payload: FileUpdate,
    service: FileService = Depends(get_file_service),
):
    return await service.update_file(file_id=file_id, title=payload.title)


@router.get("/files/{file_id}/download")
async def download_file(file_id: str, service: FileService = Depends(get_file_service)):
    file_item, stored_path = await service.get_download(file_id)
    return FileResponse(
        path=stored_path,
        media_type=file_item.mime_type,
        filename=file_item.original_name,
    )


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file_view(file_id: str, service: FileService = Depends(get_file_service)):
    await service.delete_file(file_id)
