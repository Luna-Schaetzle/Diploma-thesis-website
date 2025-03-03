# utils/ocr.py
import pytesseract
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def perform_ocr(image_path, lang='deu'):
    """
    Führt OCR auf dem gegebenen Bildpfad durch und gibt den extrahierten Text zurück.
    """
    try:
        # Bild öffnen und in Graustufen konvertieren
        image = Image.open(image_path).convert('L')  # Konvertiere zu Graustufen

        # Optional: Weitere Vorverarbeitung wie Schwellenwertsetzung
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, lang=lang, config=custom_config)
        return text
    except Exception as e:
        logger.error(f'OCR Fehler: {str(e)}')
        raise e
