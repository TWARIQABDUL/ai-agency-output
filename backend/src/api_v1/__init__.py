from flask import Blueprint

api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/v1')

from .todos import todos_bp
api_v1_bp.register_blueprint(todos_bp)