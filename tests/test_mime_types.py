from app.utils.mime_types import MIME_TO_EXT


def test_png_maps_to_dot_png():
    assert MIME_TO_EXT["image/png"] == ".png"

def test_jpeg_maps_to_dot_jpg():
    assert MIME_TO_EXT["image/jpeg"] == ".jpg"

def test_text_plain_not_in_whitelist():
    assert "text/plain" not in MIME_TO_EXT
