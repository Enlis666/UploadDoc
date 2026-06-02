MIME_TO_EXT: dict[str, str] = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",   # иногда клиенты шлют так
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/bmp": ".bmp",
    "image/tiff": ".tiff",
}

SUPPORTED_FORMATS_TEXT = "PNG, JPEG, WebP, GIF, BMP, TIFF"