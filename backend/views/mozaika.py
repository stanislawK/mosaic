from flask import Blueprint, jsonify, request

from backend.helpers.images import create_mosaic
from backend.models import MosaicModel

moz_blueprint = Blueprint('mozaika', __name__, url_prefix='/mozaika')


@moz_blueprint.route('/', methods=["GET"])
def mozaika():
    randomly = request.args.get('losowo')
    resolution = request.args.get('rozdzielczosc')
    img_urls = request.args.get('zdjecia')

    new_mosaic = MosaicModel(randomly=randomly)
    new_mosaic.add_images(img_urls)
    if resolution:
        new_mosaic.add_resolution(resolution)

    create_mosaic(new_mosaic.resolution, new_mosaic.img_urls)

    return jsonify({"msg": "losowo: {}, rozdzielczosc: {},zdjecia: {}"
                    .format(new_mosaic.randomly,
                            new_mosaic.resolution,
                            new_mosaic.img_urls)}), 200
