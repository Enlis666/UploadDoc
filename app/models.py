from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


class Documents(SQLModel, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    path: str
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DocumentsText(SQLModel, table=True):
    __tablename__ = "documents_text"

    id: int | None = Field(default=None, primary_key=True)
    id_doc: int = Field(foreign_key="documents.id")
    text: str
