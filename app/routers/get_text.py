from typing import Annotated

from fastapi import APIRouter, Query

from app.database import SessionDep
from app.schemas import GetTextResponse
from app.service.document_service import document_service

router = APIRouter()


@router.get(
    "/documents/{id}/text",
    response_model=GetTextResponse,
    summary="Получить распознанный текст",
    description="Возвращает последний текст из documents_text по id документа.",
)
def get_text(
    doc_id: Annotated[int, Query(description="ID документа", alias="id")],
    session: SessionDep,
) -> GetTextResponse:

    text = document_service.get_text(session, doc_id)

    return GetTextResponse(id=doc_id, text=text)
