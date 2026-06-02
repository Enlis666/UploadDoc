from typing import Annotated

from fastapi import APIRouter, Query

from app.database import SessionDep
from app.schemas import DeleteDocResponse
from app.service.document_service import document_service

router = APIRouter()


@router.delete(
    "/documents/{id}/delete",
    response_model=DeleteDocResponse,
    summary="Удаление документа",
)
def doc_delete(
    doc_id: Annotated[int, Query(description="ID документа", alias="id")],
    session: SessionDep,
) -> DeleteDocResponse:

    document_service.delete(session, doc_id)

    return DeleteDocResponse(message="deleted", id=doc_id)
