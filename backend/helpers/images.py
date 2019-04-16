from io import BytesIO
from math import ceil, sqrt
from PIL import Image
import requests

UPLOAD_PATH = '/mosaic/backend/static/{}.{}'


def create_mosaic(size, img_urls):
    # Create empty, white imegae bord
    mosaic = Image.new('RGB', size, color='white')
    width, height = size

    # Count coordinates for left upper corner of every pixel
    rows = ceil(sqrt(len(img_urls)))
    pixel_size = int(width/rows), int(height/rows)
    xes = [i for i in range(0, rows*pixel_size[0], pixel_size[0])]
    yes = [i for i in range(0, rows*pixel_size[1], pixel_size[1])]
    coordinates = []
    for y in yes:
        for x in xes:
            coordinates.append((x, y))

    # Connect pixels coordinates with images
    img_coord = {}
    i = 0
    while i < len(coordinates):
        img_coord[coordinates[i]] = img_urls[i % len(img_urls)]
        i += 1


def resize_images(images, size):
    """Croping and resizing given images to fit single pixel size"""
    resized = []
    for image in images:
        old_width, old_height = image.size
        if old_width > old_height:
            diff = int((old_width - old_height)/2)
            image = image.crop((diff, 0, old_width-diff, old_height))
        elif old_width < old_height:
            diff = int((old_height - old_width)/2)
            image = image.crop((0, diff, old_width, old_height-diff))
        resized_img = image.resize(size)
        resized.append(resized_img)
    return resized


def save_images(img_urls):
    for img_url in img_urls:
        name = "base_{}".format(img_urls.index(img_url), 'png')
        req = requests.get(img_url)
        img = Image.open(BytesIO(req.content))
        img.save(UPLOAD_PATH.format(name, img.format))
