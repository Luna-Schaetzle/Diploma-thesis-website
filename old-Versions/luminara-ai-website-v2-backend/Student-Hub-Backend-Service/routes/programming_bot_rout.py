# routes/programming_bot_route.py

from flask import Blueprint, request, jsonify
import logging
from config import Config
from utils.model_interaction import get_model_response  # Eine Funktion, die mit dem Modell interagiert

logger = logging.getLogger(__name__)

programming_bot_bp = Blueprint('programming_bot_bp', __name__)

@programming_bot_bp.route('/ask_programming_bot', methods=['POST'])
def ask_programming_bot():
    data = request.get_json()
    model = data.get('model')
    prompt = data.get('prompt')

    if not model or not prompt:
        logger.warning('Modell oder Prompt fehlen in der Anfrage')
        return jsonify({'error': 'Modell und Prompt sind erforderlich.'}), 400

    try:
        # Interagiere mit dem Modell
        response_text = get_model_response(model, prompt)
        return jsonify({'choices': [{'text': response_text}]})
    except Exception as e:
        logger.error(f'Fehler beim Verarbeiten der Anfrage: {str(e)}')
        return jsonify({'error': 'Fehler beim Verarbeiten der Anfrage.'}), 500
