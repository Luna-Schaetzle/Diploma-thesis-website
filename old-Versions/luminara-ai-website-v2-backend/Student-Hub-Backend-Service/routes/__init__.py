# routes/__init__.py
from flask import Blueprint

ocr_bp = Blueprint('ocr_bp', __name__)
chat_bp = Blueprint('chat_bp', __name__)

from .ocr_route import ocr_bp
from .chat_route import chat_bp
