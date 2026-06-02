from io import BytesIO
from uuid import uuid4

import pytesseract
from fastapi import UploadFile
from PIL import Image
from sqlalchemy import desc
from sqlmodel import Session, select

from app.abstractions.abc_document_service import ABCDocumentService
from app.models import Documents, DocumentsText
from app.service.errors import DocumentNotFound, TextNotReady
from app.storage import s3_storage
from app.utils.image_upload import read_upload_image


class DocumentService(ABCDocumentService):

    def _get_document_or_raise(self, session: Session, doc_id: int) -> Documents:
        doc = session.get(Documents, doc_id)
        if doc is None:
            raise DocumentNotFound(doc_id)
        return doc

    async def upload(self, session: Session, file: UploadFile) -> Documents:
        image_bytes, extension, content_type = await read_upload_image(file)
        object_key = f"documents/{uuid4()}{extension}"

        s3_storage.upload_bytes(object_key, image_bytes, content_type=content_type)

        doc = Documents(path=object_key)
        session.add(doc)
        session.commit()
        session.refresh(doc)
        return doc

    def get_text(self, session: Session, doc_id: int) -> str:
        self._get_document_or_raise(session, doc_id)

        statement = (
            select(DocumentsText)
            .where(DocumentsText.id_doc == doc_id)
            .order_by(desc(DocumentsText.id))
        )
        text_row = session.exec(statement).first()
        if text_row is None:
            raise TextNotReady(doc_id)
        return text_row.text

    def delete(self, session: Session, doc_id: int) -> None:
        doc = self._get_document_or_raise(session, doc_id)

        statement = select(DocumentsText).where(DocumentsText.id_doc == doc_id)
        for text_row in session.exec(statement).all():
            session.delete(text_row)

        s3_storage.delete_object(doc.path)
        session.delete(doc)
        session.commit()

    def enqueue_analyse(self, session: Session, doc_id: int) -> None:
        self._get_document_or_raise(session, doc_id)
        from app.tasks import analyse_document

        analyse_document.delay(doc_id)

    def run_ocr(self, session: Session, doc_id: int) -> None:
        doc = self._get_document_or_raise(session, doc_id)

        image_bytes = s3_storage.download_bytes(doc.path)
        text = pytesseract.image_to_string(Image.open(BytesIO(image_bytes)))

        session.add(DocumentsText(id_doc=doc_id, text=text))
        session.commit()


document_service = DocumentService()
