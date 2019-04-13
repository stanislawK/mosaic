from flask import Blueprint, jsonify, request

from backend.models import MosaicModel

moz_blueprint = Blueprint('mozaika', __name__, url_prefix='/mozaika')


@moz_blueprint.route('/', methods=["GET"])
def mozaika():
    randomly = request.args.get('losowo')
    resolution = request.args.get('rozdzielczosc')
    images = request.args.get('zdjecia')
    new_mosaic = MosaicModel(randomly=randomly)
    new_mosaic.add_images(images)

    if resolution:
        new_mosaic.add_resolution(resolution)

    return jsonify({"msg": "losowo: {}, rozdzielczosc: {},zdjecia: {}"
                    .format(new_mosaic.randomly,
                            new_mosaic.resolution,
                            new_mosaic.images)}), 200
