from sqlmodel import Session

from app.celery_app import celery_app
from app.database import engine
from app.service.document_service import DocumentService
from app.service.errors import DocumentNotFound


@celery_app.task
def analyse_document(doc_id: int) -> None:
    with Session(engine) as session:
        try:
            DocumentService(session).run_ocr(doc_id)
        except DocumentNotFound:
            return
