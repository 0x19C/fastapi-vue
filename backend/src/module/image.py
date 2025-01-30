from typing import IO

from PIL import Image

async def get_image_metadata(fp: IO[bytes]) -> dict:
    img = Image.open(fp)
    metadata = img._getexif()

    return metadata