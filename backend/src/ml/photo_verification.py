import base64
from PIL import Image
from io import BytesIO

from photo_handler import ImageHandler


async def photo_verification(
    profile_photo_base64: str, photo_in_base64: str
) -> bool:
    handler = ImageHandler()
    profile_photo_jpg = Image.open(BytesIO(base64.b64decode(profile_photo_base64)))
    photo_in_jpg = Image.open(BytesIO(base64.b64decode(photo_in_base64)))
    return handler.authentication(profile_photo_jpg, photo_in_jpg)