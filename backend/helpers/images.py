from io import BytesIO
from math import ceil, sqrt
from flask import send_file
from bs4 import BeautifulSoup
from PIL import Image, ImageFile
import requests

ImageFile.LOAD_TRUNCATED_IMAGES = True

img_ext = [
    'BMP',
    'EPS',
    'GIF',
    'ICO',
    'JPEG',
    'JPG',
    'JPE',
    'PNG',
    'TIFF',
    'TIF'
    ]


def check_urls(img_urls):
    """Check if given URL is direct link to img, or the entire collection"""
    for i, url in enumerate(img_urls):
        if url.split('.')[-1].upper() not in img_ext:
            img_urls.remove(url)
            new_urls = pull_urls(url)
            j = i
            for new_url in new_urls:
                if new_url.split('.')[-1].upper() != 'GIF':
                    img_urls.insert(j, new_url)
                    j += 1
        elif url.split('.')[-1].upper() == 'GIF':
            img_urls.remove(url)
    return img_urls


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

    # Pull all images urls if given url is website isted direct link
    img_urls = check_urls(img_urls)
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
    image = upload_img(img_url, size)
    old_width, old_height = image.size
    if old_width > old_height:
        diff = int((old_width - old_height)/2)
        image = image.crop((diff, 0, old_width-diff, old_height))
    elif old_width < old_height:
        diff = int((old_height - old_width)/2)
        image = image.crop((0, diff, old_width, old_height-diff))
    resized_img = image.resize(size, Image.ANTIALIAS)
    return resized_img


def upload_img(img_url, size):
    req = requests.get(img_url)
    try:
        img = Image.open(BytesIO(req.content))
    except OSError:
        img = Image.new('RGB', size, color='white')
    return img


def serve_mosaic(mosaic):
    img_io = BytesIO()
    mosaic.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
