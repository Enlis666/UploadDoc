import pytest

from app.utils.image_upload import read_upload_image, InvalidImageError


@pytest.mark.asyncio
async def test_valid_png(test_good_png_image):

    image_bytes, extension, content_type = await read_upload_image(test_good_png_image)
    assert content_type == "image/png"
    assert extension == ".png"
    assert len(image_bytes) > 0


@pytest.mark.asyncio
async def test_empty_file(test_empty_png_image):

    with pytest.raises(InvalidImageError):
        await read_upload_image(test_empty_png_image)


@pytest.mark.asyncio
async def test_bad_file(test_bat_image):

    with pytest.raises(InvalidImageError):
        await read_upload_image(test_bat_image)