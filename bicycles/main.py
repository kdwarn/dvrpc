from flask import Blueprint, redirect, url_for

main_bp = Blueprint('main_bp', __name__)  # url prefix of / set in init


@main_bp.route('/')
def main():
    return redirect(url_for('doc_bp.documentation'))
