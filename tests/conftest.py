import io
from collections.abc import Callable, Generator
from typing import Any

import pytest

from PIL import Image
from fastapi import UploadFile
from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool

@pytest.fixture
def test_good_png_image() -> UploadFile:
    """Создаёт временное тестовое PNG-изображение 100x100 пикселей."""

    img = Image.new("RGB", (100, 100), color="red")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return UploadFile(
        filename="test.png",
        file=buffer,
        headers={"content-type": "image/png"},
    )

@pytest.fixture
def test_empty_png_image() -> UploadFile:
    """Создаёт пустой файл с PNG-расшерением."""

    return UploadFile(
        filename="test.png",
        file=io.BytesIO(b""),
        headers={"content-type": "image/png"},
    )

@pytest.fixture
def test_bat_image() -> UploadFile:
    """Создаёт неподдерживаемый файл с txt-расшерением."""

    return UploadFile(
        filename="test.txt",
        file=io.BytesIO(b""),
        headers={"content-type": "text/plain"},
    )


@pytest.fixture
def session() -> Generator[Session, None, None]:
    """Создает SQLite in memory """

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def mock_s3_upload(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, bytes, str | None]]:
    calls: list[tuple[str, bytes, str | None]] = []

    def fake_upload_bytes(key: str, data: bytes, content_type: str | None = None) -> str:
        calls.append((key, data, content_type))
        return key

    monkeypatch.setattr(
        "app.service.document_service.s3_storage.upload_bytes",
        fake_upload_bytes,
    )

    return calls


@pytest.fixture
def mock_s3_delete(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    calls: list[str] = []

    def fake_delete_object(key: str) -> None:
        calls.append(key)

    monkeypatch.setattr(
        "app.service.document_service.s3_storage.delete_object",
        fake_delete_object,
    )

    return calls


@pytest.fixture
def mock_s3_download(monkeypatch: pytest.MonkeyPatch) -> dict[str, bytes]:
    box: dict[str, bytes] = {"data": b""}

    def fake_download_bytes(key: str) -> bytes:
        return box["data"]

    monkeypatch.setattr(
        "app.service.document_service.s3_storage.download_bytes",
        fake_download_bytes,
    )

    return box


@pytest.fixture
def mock_tesseract(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    box: dict[str, str] = {"text": ""}

    def fake_image_to_string(_image: Any) -> str:
        return box["text"]

    monkeypatch.setattr(
        "app.service.document_service.pytesseract.image_to_string",
        fake_image_to_string,
    )

    return box


@pytest.fixture
def mock_celery_delay(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    calls: list[int] = []

    def fake_delay(doc_id: int) -> None:
        calls.append(doc_id)

    # DocumentService imports analyse_document inside the method,
    # so patch the tasks module attribute.
    monkeypatch.setattr("app.tasks.analyse_document.delay", fake_delay)

    return calls