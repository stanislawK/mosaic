from io import BytesIO
from math import ceil, sqrt
from PIL import Image
import requests

UPLOAD_PATH = '/mosaic/backend/static/{}.{}'


def create_mosaic(size, img_urls):
    mosaic = Image.new('RGB', size, color='white')
    img_amount = len(img_urls)
    width, height = size
    rows = ceil(sqrt(len(img_urls)))
    pixel_size = width/rows, height/rows
    pixels = rows**2


def save_images(img_urls):
    for img_url in img_urls:
        name = "base_{}".format(img_urls.index(img_url), 'png')
        req = requests.get(img_url)
        img = Image.open(BytesIO(req.content))
        img.save(UPLOAD_PATH.format(name, img.format))
