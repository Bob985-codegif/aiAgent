from flask import Blueprint

book_bp = Blueprint('book', __name__)

from app.book import routes