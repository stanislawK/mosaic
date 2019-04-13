from flask import Blueprint, jsonify, request

moz_blueprint = Blueprint('mozaika', __name__, url_prefix='/mozaika')


@moz_blueprint.route('/', methods=["GET"])
def mozaika():
    randomly = request.args.get('losowo')
    resolution = request.args.get('rozdzielczosc')
    images = request.args.get('zdjecia')
    return jsonify({"msg": """losowo: {},
                    rozdzielczosc: {},
                    zdjecia: {}"""
                    .format(randomly, resolution, images)}), 200
