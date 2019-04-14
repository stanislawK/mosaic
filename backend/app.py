from flask import Flask

from backend.views import mozaika


def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object('backend.config.DevelopmentConfig')

    register_blueprints(app)
    configure_uploads(app, IMAGE_SET)

    return app


def register_blueprints(app):
    app.register_blueprint(mozaika.moz_blueprint)
