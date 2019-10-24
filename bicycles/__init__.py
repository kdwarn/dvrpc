from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# this worked, but how would I pass in the test config when just trying to run create_app?
'''
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
'''

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
