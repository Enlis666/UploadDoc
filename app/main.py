from fastapi import FastAPI

from app.database import create_db_and_tables
from app.exception_handlers import register_exception_handlers
from app.routers.doc_analyse import router as analyse_router
from app.routers.doc_delete import router as delete_router
from app.routers.get_text import router as get_text_router
from app.routers.upload_doc import router as upload_router
from app.storage import s3_storage

app = FastAPI(
    title="UploadDoc API",
    description="Загрузка в MinIO/S3, OCR через Celery, получение текста.",
)
register_exception_handlers(app)

app.include_router(upload_router)
app.include_router(delete_router)
app.include_router(analyse_router)
app.include_router(get_text_router)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()
    s3_storage.ensure_bucket()
