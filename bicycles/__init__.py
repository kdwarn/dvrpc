from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import ProductionConfig

db = SQLAlchemy()


def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    # import blueprints
    from .main import main_bp
    from .api import api_bp
    from .doc import doc_bp

    # register blueprints
    app.register_blueprint(main_bp, url_prefix="")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(doc_bp, url_prefix="/api/documentation")

    return app
