from ollama import chat, ResponseError

def test_ollama():
    try:
        system_message = {
            'role': 'system',
            'content': (
                "Du bist ein hochqualifizierter Textverarbeiter und Markdown-Experte. "
                "Deine Aufgabe ist es, den folgenden Text, der durch OCR aus einem Bild extrahiert wurde, "
                "zu verbessern und in gut strukturiertes Markdown-Format umzuwandeln. "
                "Achte dabei auf korrekte Rechtschreibung, Grammatik und Satzbau. "
                "Formatiere den Text entsprechend seiner Inhalte mit geeigneten Markdown-Elementen wie Überschriften, Listen, Codeblöcken und Hervorhebungen."
                "Gib mir NUR den Text verbessert zurück. nicht weitere Informationen."
            )
        }

        user_message = {
            'role': 'user',
            'content': (
                "Hier ist der zu verarbeitende Text:\n\n"
                "```\nDies ist ein Beispielsatz aus OCR.\n```"
            )
        }

        response = chat(
            model='qwen2.5-coder',
            messages=[system_message, user_message],
            stream=False
        )

        markdown_text = response.message.content.strip()
        print(f"Markdown:\n{markdown_text}")

    except ResponseError as e:
        print(f'Ollama ResponseError: {e.error}')
    except Exception as e:
        print(f'Ollama Fehler: {e}')

test_ollama()
