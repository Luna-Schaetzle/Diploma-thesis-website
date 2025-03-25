# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import logging
from ollama import chat, ResponseError

app = Flask(__name__)
CORS(app)

# Konfiguration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16 MB
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """
    Überprüft, ob die Datei eine erlaubte Erweiterung hat.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_ocr(image_path):
    """
    Führt OCR auf dem gegebenen Bildpfad durch und gibt den extrahierten Text zurück.
    """
    try:
        # Bild öffnen und in Graustufen konvertieren
        image = Image.open(image_path).convert('L')  # Konvertiere zu Graustufen

        # Optional: Weitere Vorverarbeitung wie Schwellenwertsetzung
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, lang='deu', config=custom_config)
        return text
    except Exception as e:
        logger.error(f'OCR Fehler: {str(e)}')
        raise e

def improve_text_with_ollama(text):
    """
    Verbessert den gegebenen Text mithilfe der Ollama API und gibt den verbesserten Markdown-Text zurück.
    """
    try:
        # Definiere die Nachrichtenstruktur mit System- und User-Rolle
        messages = [
            {
                'role': 'system',
                'content': (
                    "Du bist ein hochqualifizierter Textverarbeiter und Markdown-Experte. "
                    "Deine Aufgabe ist es, den folgenden Text, der durch OCR aus einem Bild extrahiert wurde, "
                    "zu verbessern und in gut strukturiertes Markdown-Format umzuwandeln. "
                    "Achte dabei auf korrekte Rechtschreibung, Grammatik und Satzbau. "
                    "Formatiere den Text entsprechend seiner Inhalte mit geeigneten Markdown-Elementen wie Überschriften, Listen, Codeblöcken und Hervorhebungen."
                    "Gib mir NUR den Text verbessert zurück. nicht weitere Informationen."
                )
            },
            {
                'role': 'user',
                'content': (
                    "Hier ist der zu verarbeitende Text:\n\n"
                    f"```\n{text}\n```"
                )
            }
        ]

        # Verwende die Ollama Bibliothek, um eine Chat-Antwort zu generieren
        response = chat(
            model='qwen2.5-coder:0.5b',  # Ersetze dies durch den tatsächlichen Modellnamen
            messages=messages,
            stream=False
        )

        # Überprüfe die Antwort und extrahiere den Markdown-Text
        markdown_text = response.message.content.strip()

        if not markdown_text:
            logger.error('Ollama hat keinen Text zurückgegeben.')
            raise Exception('Ollama konnte den Text nicht verbessern.')

        return markdown_text

    except ResponseError as e:
        logger.error(f'Ollama ResponseError: {e.error}')
        raise e
    except Exception as e:
        logger.error(f'Ollama Fehler: {str(e)}')
        raise e

def convert_to_markdown(text):
    """
    Diese Funktion nimmt den verbesserten Text und stellt sicher, dass er im Markdown-Format ist.
    Momentan gibt sie den Text unverändert zurück, kann aber bei Bedarf erweitert werden.
    """
    try:
        # Wenn zusätzliche Verarbeitung erforderlich ist, kann dies hier hinzugefügt werden
        return text
    except Exception as e:
        logger.error(f'Markdown Konvertierungsfehler: {str(e)}')
        raise e

@app.route('/api/ocr', methods=['POST'])
def ocr_endpoint():
    """
    OCR Endpunkt: Nimmt ein Bild entgegen, führt OCR durch, verbessert den Text mit Ollama und gibt beide Versionen zurück.
    """
    if 'image' not in request.files:
        logger.warning('Kein Bild bereitgestellt')
        return jsonify({'error': 'Kein Bild bereitgestellt'}), 400

    file = request.files['image']

    if file.filename == '':
        logger.warning('Kein ausgewähltes Bild')
        return jsonify({'error': 'Kein ausgewähltes Bild'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f'Bild gespeichert: {filepath}')

        try:
            # OCR durchführen
            ocr_text = perform_ocr(filepath)
            logger.info(f'OCR Extrahierter Text: {ocr_text}')

            if not ocr_text.strip():
                logger.warning('OCR hat keinen Text gefunden')
                return jsonify({'error': 'OCR hat keinen Text gefunden'}), 400

            # Text mit Ollama verbessern
            improved_text = improve_text_with_ollama(ocr_text)
            logger.info(f'Verbesserter Text: {improved_text}')

            if not improved_text.strip():
                logger.warning('Ollama hat den Text nicht verbessert')
                return jsonify({'error': 'Ollama hat den Text nicht verbessert'}), 500

            # In Markdown umwandeln
            markdown_text = convert_to_markdown(improved_text)
            logger.info('Markdown generiert')

            # Rückgabe beider Versionen
            return jsonify({
                'ocr_text': ocr_text,
                'markdown': markdown_text
            }), 200
        except ResponseError as e:
            logger.error(f'Ollama ResponseError: {e.error}')
            return jsonify({'error': f'Ollama API Fehler: {e.error}'}), e.status_code
        except Exception as e:
            logger.error(f'Fehler bei der Verarbeitung: {str(e)}')
            return jsonify({'error': str(e)}), 500
        finally:
            # Optional: Lösche das hochgeladene Bild nach der Verarbeitung
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f'Bild gelöscht: {filepath}')
    else:
        logger.warning('Ungültiger Dateityp')
        return jsonify({'error': 'Ungültiger Dateityp'}), 400

if __name__ == '__main__':
    # Starte die Flask-App auf allen verfügbaren IP-Adressen (0.0.0.0) und Port 5000
    app.run(host='0.0.0.0', port=5000)
