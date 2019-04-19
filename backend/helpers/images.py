from flask import send_file
from io import BytesIO
from math import ceil, sqrt
from PIL import Image
import requests


def pull_urls(site):
    """If URL isn't direct image link, pull all image urls from website"""
    r = requests.get(site)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img.get('src') for img in img_tags]

    # In case of relative image sources
    for i, url in enumerate(img_urls):
        if 'http' not in url:
            img_urls[i] = '{}{}'.format(site, url)
    return img_urls


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

    # Paste images into mosaic
    pixel_size = pixel_side, pixel_side
    for pixel in img_coord.items():
        mosaic.paste(resize_img(pixel[1], pixel_size), pixel[0])

    return mosaic


def resize_img(img_url, size):
    """Croping and resizing given image to fit single pixel size"""
    image = upload_img(img_url)
    old_width, old_height = image.size
    if old_width > old_height:
        diff = int((old_width - old_height)/2)
        image = image.crop((diff, 0, old_width-diff, old_height))
    elif old_width < old_height:
        diff = int((old_height - old_width)/2)
        image = image.crop((0, diff, old_width, old_height-diff))
    resized_img = image.resize(size, Image.ANTIALIAS)
    return resized_img


def upload_img(img_url):
    req = requests.get(img_url)
    img = Image.open(BytesIO(req.content))
    return img


def serve_mosaic(mosaic):
    img_io = BytesIO()
    mosaic.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
