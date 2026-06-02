from pathlib import Path

from fastapi import UploadFile

from app.utils.mime_types import MIME_TO_EXT, SUPPORTED_FORMATS_TEXT

class InvalidImageError(ValueError):
    pass

EXT_TO_MIME = {ext: mime for mime, ext in MIME_TO_EXT.items()}


async def read_upload_image(file: UploadFile) -> tuple[bytes, str, str]:
    image_bytes = await file.read()
    if not image_bytes:
        raise InvalidImageError("Файл пустой")

    content_type = file.content_type
    extension = MIME_TO_EXT.get(content_type) if content_type else None

    if extension is None and file.filename:
        suffix = Path(file.filename).suffix.lower()
        if suffix in EXT_TO_MIME:
            extension = suffix
            content_type = EXT_TO_MIME[suffix]

    if extension is None:
        raise InvalidImageError(
            f"Неподдерживаемый формат. Поддерживаются: {SUPPORTED_FORMATS_TEXT}"
        )

    if not content_type:
        content_type = next(
            (m for m, e in MIME_TO_EXT.items() if e == extension),
            "application/octet-stream",
        )

    return image_bytes, extension, content_type