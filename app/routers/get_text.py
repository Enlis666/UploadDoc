from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.schemas import GetTextResponse
from app.service.document_service import DocumentService, get_document_service

router = APIRouter()


@router.get(
    "/documents/{id}/text",
    response_model=GetTextResponse,
    summary="Получить распознанный текст",
    description="Возвращает последний текст из documents_text по id документа.",
)
def get_text(
    doc_id: Annotated[int, Query(description="ID документа", alias="id")],
    service: DocumentService = Depends(get_document_service),
) -> GetTextResponse:

    text = service.get_text(doc_id)

    return GetTextResponse(id=doc_id, text=text)
