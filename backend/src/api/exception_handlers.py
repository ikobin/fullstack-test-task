from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from src.core.exceptions import EmptyFileError, NotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.message})

    @app.exception_handler(EmptyFileError)
    async def empty_file_handler(_: Request, exc: EmptyFileError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.message})
