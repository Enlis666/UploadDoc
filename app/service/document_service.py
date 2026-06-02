from io import BytesIO
from uuid import uuid4

import pytesseract
from fastapi import UploadFile
from PIL import Image
from sqlalchemy import desc
from sqlmodel import Session, select

from app.abstractions.abc_document_service import ABCDocumentService
from app.database import SessionDep
from app.models import Documents, DocumentsText
from app.service.errors import DocumentNotFound, TextNotReady
from app.storage import s3_storage
from app.utils.image_upload import read_upload_image


class DocumentService(ABCDocumentService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self._session = session

    def _get_document_or_raise(self, doc_id: int) -> Documents:
        doc = self._session.get(Documents, doc_id)
        if doc is None:
            raise DocumentNotFound(doc_id)
        return doc

    async def upload(self, file: UploadFile) -> Documents:
        image_bytes, extension, content_type = await read_upload_image(file)
        object_key = f"documents/{uuid4()}{extension}"

        s3_storage.upload_bytes(object_key, image_bytes, content_type=content_type)

        doc = Documents(path=object_key)
        self._session.add(doc)
        self._session.commit()
        self._session.refresh(doc)
        return doc

    def get_text(self, doc_id: int) -> str:
        self._get_document_or_raise(doc_id)

        statement = (
            select(DocumentsText)
            .where(DocumentsText.id_doc == doc_id)
            .order_by(desc(DocumentsText.id))
        )
        text_row = self._session.exec(statement).first()
        if text_row is None:
            raise TextNotReady(doc_id)
        return text_row.text

    def delete(self, doc_id: int) -> None:
        doc = self._get_document_or_raise(doc_id)

        statement = select(DocumentsText).where(DocumentsText.id_doc == doc_id)
        for text_row in self._session.exec(statement).all():
            self._session.delete(text_row)

        s3_storage.delete_object(doc.path)
        self._session.delete(doc)
        self._session.commit()

    def enqueue_analyse(self, doc_id: int) -> None:
        self._get_document_or_raise(doc_id)
        from app.tasks import analyse_document

        analyse_document.delay(doc_id)

    def run_ocr(self, doc_id: int) -> None:
        doc = self._get_document_or_raise(doc_id)

        image_bytes = s3_storage.download_bytes(doc.path)
        text = pytesseract.image_to_string(Image.open(BytesIO(image_bytes)))

        self._session.add(DocumentsText(id_doc=doc_id, text=text))
        self._session.commit()


def get_document_service(session: SessionDep) -> DocumentService:
    return DocumentService(session)
