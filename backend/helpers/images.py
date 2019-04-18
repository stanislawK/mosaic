from io import BytesIO
from math import ceil, sqrt
from PIL import Image
import requests

UPLOAD_PATH = '/mosaic/backend/static/{}.{}'


def create_mosaic(size, img_urls):
    # Create empty, white imegae bord
    mosaic = Image.new('RGB', size, color='white')
    width, height = size
    imgs_amount = len(img_urls)

    # Count coordinates for left upper corner of every pixel
    if width > height:
        pixel_side = int(sqrt(width*height/imgs_amount))
        columns = ceil(width/pixel_side)
        rows = ceil(imgs_amount/columns)
    elif width < height:
        pixel_side = int(sqrt(width*height/imgs_amount))
        rows = columns = ceil(height/pixel_side)
        columns = ceil(imgs_amount/rows)
    else:
        rows = columns = ceil(sqrt(imgs_amount))

    pixel_side = int(width/columns)
    xes = [i for i in range(0, columns*pixel_side, pixel_side)]
    yes = [i for i in range(0, rows*pixel_side, pixel_side)]
    coordinates = []
    for y in yes:
        for x in xes:
            coordinates.append((x, y))

    # Connect pixels coordinates with images
    img_coord = {}
    i = 0
    while i < len(coordinates):
        img_coord[coordinates[i]] = img_urls[i % imgs_amount]
        i += 1

    return img_coord


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
