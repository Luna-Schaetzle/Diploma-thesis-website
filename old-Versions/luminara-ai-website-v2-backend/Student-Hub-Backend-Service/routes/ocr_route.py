# routes/ocr_route.py

from flask import Blueprint, request, jsonify
import logging
import os
from config import Config
from utils.text_processing import improve_text_with_ollama
from PIL import Image
from io import BytesIO
import base64
import pytesseract  # Stelle sicher, dass pytesseract installiert ist

logger = logging.getLogger(__name__)

ocr_bp = Blueprint('ocr_bp', __name__)

def allowed_file(filename):
    """
    Checks if the file has an allowed extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@ocr_bp.route('/ocr', methods=['POST'])
def process_ocr():
    """
    OCR endpoint: Accepts an image (as a Base64 string or as a file), extracts text using OCR,
    improves the text with Ollama, and returns both the raw and improved text.
    Supports both JSON and multipart/form-data requests.
    """
    img_path = None  # Initialisiere img_path für die Cleanup
    try:
        # Prüfe, ob die Anfrage JSON-Daten enthält
        if request.is_json:
            data = request.get_json()
            image_str = data.get('image')

            if not image_str:
                logger.warning('Bilddaten fehlen in JSON-Anfrage')
                return jsonify({'error': 'Bilddaten fehlen'}), 400

            # Dekodiere das Base64-Bild
            if ',' in image_str:
                header, encoded = image_str.split(',', 1)
            else:
                header, encoded = '', image_str
            try:
                img_data = base64.b64decode(encoded)
                img = Image.open(BytesIO(img_data))
            except Exception as e:
                logger.error(f'Fehler beim Dekodieren des Base64-Bildes: {str(e)}')
                return jsonify({'error': 'Ungültige Base64-Bilddaten'}), 400

        else:
            # Annahme: multipart/form-data Anfrage
            if 'image' not in request.files:
                logger.warning('Keine Bilddatei in multipart/form-data-Anfrage bereitgestellt')
                return jsonify({'error': 'Keine Bilddatei bereitgestellt'}), 400

            file = request.files['image']

            if file.filename == '':
                logger.warning('Leerer Dateiname in multipart/form-data-Anfrage')
                return jsonify({'error': 'Leerer Dateiname'}), 400

            if file and allowed_file(file.filename):
                try:
                    img = Image.open(file.stream)
                except Exception as e:
                    logger.error(f'Fehler beim Öffnen der hochgeladenen Bilddatei: {str(e)}')
                    return jsonify({'error': 'Ungültige Bilddatei'}), 400
            else:
                logger.warning(f'Ungültiges Bildformat: {file.filename}')
                return jsonify({'error': f'Ungültiges Bildformat. Erlaubt: {", ".join(Config.ALLOWED_EXTENSIONS)}'}), 400

        # Validierung des Bildformats
        if img.format.lower() not in Config.ALLOWED_EXTENSIONS:
            logger.warning(f'Ungültiges Bildformat: {img.format}')
            return jsonify({'error': f'Ungültiges Bildformat: {img.format}'}), 400

        # Optional: Bildgröße reduzieren oder komprimieren
        img.thumbnail((1024, 1024))  # Beispiel: Maximale Größe 1024x1024

        # Speichere das Bild temporär, falls dein OCR-Tool dies benötigt
        img_filename = "temp_ocr.png"
        img_path = os.path.join(Config.UPLOAD_FOLDER, img_filename)
        try:
            img.save(img_path)
        except Exception as e:
            logger.error(f'Fehler beim Speichern des temporären Bildes: {str(e)}')
            return jsonify({'error': 'Fehler beim Speichern des Bildes'}), 500

        # Führe OCR durch
        try:
            # Extrahiere den rohen Text mittels Tesseract
            extrahierter_text = pytesseract.image_to_string(img, lang=Config.TESSERACT_LANG)
            if not extrahierter_text.strip():
                logger.warning('OCR konnte keinen Text extrahieren')
                return jsonify({'error': 'OCR konnte keinen Text extrahieren'}), 400
        except Exception as e:
            logger.error(f'Fehler bei der OCR-Verarbeitung: {str(e)}')
            return jsonify({'error': 'Fehler bei der OCR-Verarbeitung'}), 500

        # Verbessere den Text mit Ollama
        try:
            verbesserter_text = improve_text_with_ollama(extrahierter_text, model='llama3.2')
        except Exception as e:
            logger.error(f'Fehler beim Verbessern des Textes mit Ollama: {str(e)}')
            return jsonify({'error': 'Fehler beim Verbessern des Textes'}), 500

        return jsonify({
            'raw_text': extrahierter_text,
            'improved_text': verbesserter_text
        }), 200

    except Exception as e:
        logger.error(f'Allgemeiner Fehler im OCR-Endpunkt: {str(e)}')
        return jsonify({'error': f'Allgemeiner Fehler: {str(e)}'}), 500

    finally:
        # Bereinige das temporäre Bild
        if img_path and os.path.exists(img_path):
            try:
                os.remove(img_path)
            except Exception as e:
                logger.error(f'Fehler beim Entfernen des temporären Bildes: {str(e)}')
