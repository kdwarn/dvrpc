from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)  # url prefix of / set in init

@main_bp.route('/', methods=['GET'])
def hello():
    return "hello world!"
