import pytest
from sqlmodel import select

from app.models import Documents, DocumentsText
from app.service.document_service import DocumentService
from app.service.errors import DocumentNotFound, TextNotReady


@pytest.mark.asyncio
async def test_valid_png_upload(test_good_png_image, session, mock_s3_upload):
    doc = await DocumentService(session).upload(test_good_png_image)
    key, data, content_type = mock_s3_upload[0]

    assert key == doc.path
    assert key.startswith("documents/")
    assert len(data) > 0
    assert content_type == "image/png"
    assert doc.id is not None


def test_get_text_document_not_found(session):
    with pytest.raises(DocumentNotFound) as exc:
        DocumentService(session).get_text(999)
    assert exc.value.doc_id == 999


def test_get_text_text_not_ready(session):
    doc = Documents(path="documents/test.png")
    session.add(doc)
    session.commit()
    session.refresh(doc)

    with pytest.raises(TextNotReady) as exc:
        DocumentService(session).get_text(doc.id)
    assert exc.value.doc_id == doc.id


def test_get_text_returns_latest_text(session):
    doc = Documents(path="documents/test.png")
    session.add(doc)
    session.commit()
    session.refresh(doc)

    session.add(DocumentsText(id_doc=doc.id, text="old"))
    session.add(DocumentsText(id_doc=doc.id, text="new"))
    session.commit()

    assert DocumentService(session).get_text(doc.id) == "new"


def test_delete_document_not_found(session):
    with pytest.raises(DocumentNotFound):
        DocumentService(session).delete(999)


def test_delete_removes_doc_and_calls_s3(session, mock_s3_delete):
    doc = Documents(path="documents/to-delete.png")
    session.add(doc)
    session.commit()
    session.refresh(doc)

    session.add(DocumentsText(id_doc=doc.id, text="t1"))
    session.add(DocumentsText(id_doc=doc.id, text="t2"))
    session.commit()

    DocumentService(session).delete(doc.id)

    assert session.get(Documents, doc.id) is None
    assert mock_s3_delete == [doc.path]


def test_enqueue_analyse_document_not_found(session):
    with pytest.raises(DocumentNotFound):
        DocumentService(session).enqueue_analyse(999)


def test_enqueue_analyse_calls_delay(session, mock_celery_delay):
    doc = Documents(path="documents/a.png")
    session.add(doc)
    session.commit()
    session.refresh(doc)

    DocumentService(session).enqueue_analyse(doc.id)
    assert mock_celery_delay == [doc.id]


def test_run_ocr_document_not_found(session):
    with pytest.raises(DocumentNotFound):
        DocumentService(session).run_ocr(999)


def test_run_ocr_saves_text(session, mock_s3_download, mock_tesseract):
    doc = Documents(path="documents/ocr.png")
    session.add(doc)
    session.commit()
    session.refresh(doc)

    # Minimal valid PNG bytes (1x1) so PIL can open it.
    mock_s3_download["data"] = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\x0bIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
        b"\x0d\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    mock_tesseract["text"] = "hello"

    DocumentService(session).run_ocr(doc.id)

    rows = session.exec(select(DocumentsText).where(DocumentsText.id_doc == doc.id)).all()
    assert len(rows) == 1
    assert rows[0].text == "hello"