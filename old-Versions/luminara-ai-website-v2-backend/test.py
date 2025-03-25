import pytesseract
from PIL import Image

def test_ocr(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='deu')
        print(f'OCR Text: {text}')
    except Exception as e:
        print(f'OCR Fehler: {e}')

test_ocr('/home/luna/Bilder/Bildschirmfotos/Bildschirmfoto vom 2024-09-27 20-45-19.png')
