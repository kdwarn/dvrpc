from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)  # url prefix of / set in init

@main_bp.route('/')
def hello():
    return "Brief intro will go here"
