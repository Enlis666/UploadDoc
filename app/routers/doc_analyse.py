from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.schemas import DocAnalyseResponse
from app.service.document_service import DocumentService, get_document_service

router = APIRouter()


@router.get(
    "/documents/{id}/analysis",
    response_model=DocAnalyseResponse,
    summary="Анализ текста на фото",
    description="Ставит задачу Celery: OCR изображения из S3 и запись в documents_text.",
)
def doc_analyse(
    doc_id: Annotated[int, Query(description="ID документа", alias="id")],
    service: DocumentService = Depends(get_document_service),
) -> DocAnalyseResponse:

    service.enqueue_analyse(doc_id)

    return DocAnalyseResponse(status="accepted", id=doc_id)
