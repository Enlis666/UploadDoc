from abc import ABC, abstractmethod

from fastapi import UploadFile
from sqlmodel import Session

from app.models import Documents


class ABCDocumentService(ABC):

    @abstractmethod
    async def upload(self, session: Session, file: UploadFile) -> Documents:
        pass

    @abstractmethod
    def get_text(self, session: Session, doc_id: int) -> str:
        pass

    @abstractmethod
    def delete(self, session: Session, doc_id: int) -> None:
        pass

    @abstractmethod
    def enqueue_analyse(self, session: Session, doc_id: int) -> None:
        pass

    @abstractmethod
    def run_ocr(self, session: Session, doc_id: int) -> None:
        pass
