# utils/markdown_converter.py
import logging

logger = logging.getLogger(__name__)

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
