from flask import jsonify, Blueprint

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def index():
    return jsonify(message='Welcome to the API!')