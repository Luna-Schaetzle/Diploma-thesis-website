# routes/chat_route.py
from flask import Blueprint, request, jsonify
import logging
import os
from config import Config
from utils.text_processing import ask_ollama, ask_ollama_vision
from PIL import Image
from io import BytesIO
import base64

# Füge diese Zeilen hinzu:
from ollama import chat, ResponseError

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat_bp', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@chat_bp.route('/ask_ollama', methods=['POST'])
def ask_ollama_endpoint():
    """
    Chat-Endpunkt: Nimmt eine Benutzeranfrage und ein Modell, kommuniziert mit Ollama und gibt die Antwort zurück.
    """
    data = request.get_json()

    if not data:
        logger.warning('Keine JSON-Daten bereitgestellt')
        return jsonify({'error': 'Keine JSON-Daten bereitgestellt'}), 400

    prompt = data.get('prompt')
    model = data.get('model', Config.OLLAMA_MODEL_DEFAULT)  # Standardmodell

    if not prompt:
        logger.warning('Prompt fehlt')
        return jsonify({'error': 'Prompt fehlt'}), 400

    try:
        response = ask_ollama(prompt, model=model)

        if 'choices' in response:
            return jsonify(response), 200
        else:
            return jsonify(response), 500

    except Exception as e:
        logger.error(f'Fehler beim Kommunizieren mit Ollama: {str(e)}')
        return jsonify({'error': 'Fehler beim Kommunizieren mit Ollama'}), 500


@chat_bp.route('/ask_ollama_vision', methods=['POST'])
def ask_ollama_vision_endpoint():
    """
    Vision-Chat-Endpunkt: Nimmt eine Benutzeranfrage mit Bildern und einem Modell, kommuniziert mit Ollama Vision und gibt die Antwort zurück.
    """
    data = request.get_json()

    if not data:
        logger.warning('Keine JSON-Daten bereitgestellt')
        return jsonify({'error': 'Keine JSON-Daten bereitgestellt'}), 400

    prompt = data.get('prompt')
    model = data.get('model', 'llama3.2-vision')  # Standardmodell für Vision
    images = data.get('images', [])

    if not prompt and not images:
        logger.warning('Weder Prompt noch Bilder bereitgestellt')
        return jsonify({'error': 'Weder Prompt noch Bilder bereitgestellt'}), 400

    # Verarbeite die Bilder
    image_paths = []
    try:
        for idx, img_str in enumerate(images):
            # Dekodiere das Base64-Bild
            if ',' in img_str:
                header, encoded = img_str.split(',', 1)
            else:
                header, encoded = '', img_str
            img_data = base64.b64decode(encoded)
            img = Image.open(BytesIO(img_data))

            # Validierung des Bildformats
            if img.format.lower() not in Config.ALLOWED_EXTENSIONS:
                logger.warning(f'Ungültiges Bildformat: {img.format}')
                return jsonify({'error': f'Ungültiges Bildformat: {img.format}'}), 400

            # Optional: Bildgröße reduzieren oder komprimieren
            img.thumbnail((1024, 1024))  # Beispiel: Maximale Größe 1024x1024

            # Speichere das Bild temporär
            img_filename = f"temp_{idx}.{img.format.lower()}"
            img_path = os.path.join(Config.UPLOAD_FOLDER, img_filename)
            img.save(img_path)
            image_paths.append(img_path)

    except Exception as e:
        logger.error(f'Fehler beim Verarbeiten der Bilder: {str(e)}')
        return jsonify({'error': f'Fehler beim Verarbeiten der Bilder: {str(e)}'}), 400

    try:
        response = ask_ollama_vision(prompt, model=model, image_paths=image_paths)

        if 'choices' in response:
            return jsonify(response), 200
        else:
            return jsonify(response), 500

    except Exception as e:
        logger.error(f'Fehler beim Kommunizieren mit Ollama Vision: {str(e)}')
        return jsonify({'error': 'Fehler beim Kommunizieren mit Ollama Vision'}), 500

    finally:
        # Bereinige die temporären Bilder
        for img_path in image_paths:
            if os.path.exists(img_path):
                os.remove(img_path)


@chat_bp.route('/ask_programming_bot', methods=['POST'])
def ask_programming_bot_endpoint():
    """
    Programmierbot-Endpunkt: Nimmt eine Benutzeranfrage, kommuniziert mit Ollama und gibt die Antwort zurück.
    """
    data = request.get_json()

    if not data:
        logger.warning('Keine JSON-Daten bereitgestellt')
        return jsonify({'error': 'Keine JSON-Daten bereitgestellt'}), 400

    prompt = data.get('prompt')
    model = data.get('model', 'qwen2.5-coder:0.5b')

    if not prompt:
        logger.warning('Prompt fehlt')
        return jsonify({'error': 'Prompt fehlt'}), 400

    try:
        # Definiere eine spezielle Systemnachricht für den Programmierbot
        messages = [
            {
                'role': 'system',
                'content': (
                    "Du bist ein erfahrene Programmiererin und technische Beraterin namens Luminara."
                    "Beantworte Programmierfragen präzise und liefere klare Codebeispiele in der gefragten Programmiersprache."
                )
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        # Sende die Anfrage an Ollama
        response = chat(
            model=model,
            messages=messages,
            stream=False
        )

        # Extrahiere die Antwort
        bot_response = response.message.content.strip()

        if not bot_response:
            logger.error('Ollama hat keine Antwort zurückgegeben.')
            raise Exception('Ollama konnte keine Antwort generieren.')

        return {'choices': [{'text': bot_response}]}

    except ResponseError as e:
        logger.error(f'Ollama ResponseError: {e.error}')
        return jsonify({'error': f'Ollama API Fehler: {e.error}'}), 500
    except Exception as e:
        logger.error(f'Ollama Fehler: {str(e)}')
        return jsonify({'error': str(e)}), 500

