# config.py
import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    TESSERACT_LANG = 'deu'  # Deutsch
    OLLAMA_MODEL_DEFAULT = 'llama3.2:1b'  # Standardmodell für den Chatbot
