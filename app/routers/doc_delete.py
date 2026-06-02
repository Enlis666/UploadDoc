from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.schemas import DeleteDocResponse
from app.service.document_service import DocumentService, get_document_service

router = APIRouter()


@router.delete(
    "/documents/{id}/delete",
    response_model=DeleteDocResponse,
    summary="Удаление документа",
)
def doc_delete(
    doc_id: Annotated[int, Query(description="ID документа", alias="id")],
    service: DocumentService = Depends(get_document_service),
) -> DeleteDocResponse:

    service.delete(doc_id)

    return DeleteDocResponse(message="deleted", id=doc_id)
