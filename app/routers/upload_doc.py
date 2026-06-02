from fastapi import APIRouter, Depends, File, UploadFile

from app.schemas import UploadDocResponse
from app.service.document_service import DocumentService, get_document_service

router = APIRouter()


@router.post(
    "/documents/upload",
    response_model=UploadDocResponse,
    summary="Загрузка документа",
    description="Принимает изображение (PNG, JPEG, WebP, ...), сохраняет в MinIO/S3.",
)
async def upload_doc(
    service: DocumentService = Depends(get_document_service),
    file: UploadFile = File(..., description="PNG, JPEG, WebP, ..."),
) -> UploadDocResponse:
    doc = await service.upload(file)
    return UploadDocResponse(id=doc.id, path=doc.path)
