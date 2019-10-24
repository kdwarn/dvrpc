from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    # import blueprints
    from .api import api_bp
    from .main import main_bp

    # register blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(main_bp, url_prefix="")

    return app
