from flask import Flask


def create_app():
    """Application factory function."""
    app = Flsk(__name__)
    app.config.from_object('backend.config.DevelopmentConfig')

    return app
