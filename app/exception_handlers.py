from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.service.errors import DocumentNotFound, TextNotReady
from app.utils.image_upload import InvalidImageError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DocumentNotFound)
    def handle_document_not_found(
        _request: Request, exc: DocumentNotFound
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Документ {exc.doc_id} не найден"},
        )

    @app.exception_handler(TextNotReady)
    def handle_text_not_ready(_request: Request, exc: TextNotReady) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Текст ещё не готов. Сначала вызовите /doc_analyse",
            },
        )

    @app.exception_handler(InvalidImageError)
    def handle_invalid_image(_request: Request, exc: InvalidImageError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})
