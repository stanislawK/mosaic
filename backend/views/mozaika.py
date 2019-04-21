from flask import Blueprint, jsonify, request
import requests

from backend.helpers.images import create_mosaic, serve_mosaic
from backend.models import MosaicModel

URL_NOT_FOUND = "Please provide valid URL address with images"

moz_blueprint = Blueprint('mozaika', __name__, url_prefix='/mozaika')


@moz_blueprint.route('/', methods=["GET"])
def mozaika():
    randomly = request.args.get('losowo')
    resolution = request.args.get('rozdzielczosc')
    img_urls = request.args.get('zdjecia')

    new_mosaic = MosaicModel(randomly=randomly)

    if img_urls:
        new_mosaic.add_images(img_urls)
    else:
        return jsonify({"msg": URL_NOT_FOUND}), 404

    if resolution:
        new_mosaic.add_resolution(resolution)

    try:
        mosaic = create_mosaic(new_mosaic.resolution, new_mosaic.img_urls)
        return serve_mosaic(mosaic), 200

    except (TypeError, ZeroDivisionError, requests.exceptions.MissingSchema):
        return jsonify({"msg": URL_NOT_FOUND}), 404
