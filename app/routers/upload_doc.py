from fastapi import APIRouter, File, UploadFile

from app.database import SessionDep
from app.schemas import UploadDocResponse
from app.service.document_service import document_service

router = APIRouter()


@router.post(
    "/documents/upload",
    response_model=UploadDocResponse,
    summary="Загрузка документа",
    description="Принимает изображение (PNG, JPEG, WebP, ...), сохраняет в MinIO/S3.",
)
async def upload_doc(
    session: SessionDep,
    file: UploadFile = File(..., description="PNG, JPEG, WebP, ..."),
) -> UploadDocResponse:
    doc = await document_service.upload(session, file)
    return UploadDocResponse(id=doc.id, path=doc.path)
