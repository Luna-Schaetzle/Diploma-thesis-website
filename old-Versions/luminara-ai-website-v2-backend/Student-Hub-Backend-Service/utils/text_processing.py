# utils/text_processing.py

from ollama import chat, ResponseError
import logging
from PIL import Image
from io import BytesIO
import base64
import os

logger = logging.getLogger(__name__)

def improve_text_with_ollama(text, model='llama3.2'):  #Das Modell könnte man hier ändern zum Beispiel auf 'llama3.2:1b' oder 'qwen2.5-coder'
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
                    "Formatiere den Text entsprechend seiner Inhalte mit geeigneten Markdown-Elementen wie Überschriften, Listen, Codeblöcken und Hervorhebungen. "
                    "Antworten Sie mit dem verbesserten Markdown-Text, und nur dem Text, ohne zusätzliche Kommentare oder Erklärungen."
                    "Antworte nur mit dem Verbesserten Text, ohne zusätzliche Kommentare oder Erklärungen."
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
            model=model,
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

def ask_ollama(prompt, model='llama3.2:1b'):
    """
    Sendet eine Benutzeranfrage an das ausgewählte Ollama-Modell und gibt die Antwort zurück.
    """
    try:
        # Definiere die Nachrichtenstruktur
        messages = [
            {
                'role': 'system',
                'content': 'Du bist ein hilfreicher Assistent. Bitte beantworte die folgende Benutzeranfrage:'
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
        return {'error': f'Ollama API Fehler: {e.error}'}
    except Exception as e:
        logger.error(f'Ollama Fehler: {str(e)}')
        return {'error': str(e)}

def ask_ollama_vision(prompt, model='llama3.2-vision', image_paths=[]):
    """
    Sendet eine Benutzeranfrage mit Bildern an das ausgewählte Ollama-Modell und gibt die Antwort zurück.
    """
    try:
        # Definiere die Nachrichtenstruktur mit Bildern
        messages = [
            {
                'role': 'user',
                'content': prompt,
                'images': image_paths  # Liste der Bildpfade
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
        return {'error': f'Ollama API Fehler: {e.error}'}
    except Exception as e:
        logger.error(f'Ollama Fehler: {str(e)}')
        return {'error': str(e)}
