import ollama as ollama

def improve_text_with_ollama(text):
    """
    Verbessert den gegebenen Text mit Ollama.
    """
    try:
        improved_text = ollama.improve_text(text)
        return improved_text
    except Exception as e:
        raise e