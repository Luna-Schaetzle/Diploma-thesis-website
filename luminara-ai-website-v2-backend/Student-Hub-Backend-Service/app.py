# app.py
from flask import Flask
from flask_cors import CORS
import os
import logging

from config import Config
from routes import ocr_bp, chat_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Konfiguriere die Anwendung
    app.config.from_object(Config)

    # Registriere Blueprints
    app.register_blueprint(ocr_bp)
    app.register_blueprint(chat_bp)

    # Richte das Upload-Verzeichnis ein
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Logging konfigurieren
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Flask OCR und Chat App gestartet.")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
