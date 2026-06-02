from abc import ABC, abstractmethod

from fastapi import UploadFile
from sqlmodel import Session

from app.models import Documents


class ABCDocumentService(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    async def upload(self, file: UploadFile) -> Documents:
        pass

    @abstractmethod
    def get_text(self, doc_id: int) -> str:
        pass

    @abstractmethod
    def delete(self, doc_id: int) -> None:
        pass

    @abstractmethod
    def enqueue_analyse(self, doc_id: int) -> None:
        pass

    @abstractmethod
    def run_ocr(self, doc_id: int) -> None:
        pass
