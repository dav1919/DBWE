from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes  # This import must be at the bottom to avoid circular imports
