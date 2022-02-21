import base64
from io import BytesIO

from PIL import Image

from django.conf import settings
from yandex_geocoder import Client


def watermark_image(image, position=(0, 0)):
    """Add a watermark to Image"""
    watermark_size_300 = (300, 300)
    watermark = Image.open('static/watermark/Untitled.png', mode='r')
    watermark.thumbnail(watermark_size_300)

    base_image = Image.open(image)
    base_image.paste(watermark, position)
    base_image.save(image)

    buffered = BytesIO()
    base_image.save(buffered, format='PNG')
    img_str = base64.b64encode(buffered.getvalue())

    return img_str


def get_location(adress):
    """Get coordinates from adress string"""
    client = Client(settings.YANDEX_GEOCODER_API_KEY)
    coordinates = client.coordinates(adress)
    latitude = float(coordinates[0])
    longitude = float(coordinates[1])
    pnt = f"POINT({latitude} {longitude})"

    return pnt
