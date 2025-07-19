import cv2
import pytesseract
from deep_translator import GoogleTranslator
import numpy as np
import os
import shutil
from uuid import uuid4

# Optional: set path if tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

OCR_LANGS = "eng+hin+ben+kan+tam+tel+guj+mar+pan+urd"

def process_image(file_path: str, target_lang: str = "en") -> dict:
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError("Invalid image")

    text = pytesseract.image_to_string(image, lang=OCR_LANGS).strip()
    if not text:
        return {"extracted": "", "translated": "", "error": "No text found"}

    translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
    return {
        "extracted": text,
        "translated": translated,
        "error": None
    }
