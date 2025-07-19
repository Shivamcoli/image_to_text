# pip install pytesseract
# pip install opencv-python
# pip install deep-translator

import cv2
import pytesseract
from deep_translator import GoogleTranslator
import numpy as np
import os

# ========== CONFIG ==========
IMAGE_PATH = "image.jpg"          # Change this to your image file
TARGET_LANG = "en"                # Output translation language
OCR_LANGS = "eng+hin+ben+kan+tam+tel+guj+mar+pan+urd"  # Add more if needed
# ============================

# Windows users: Uncomment and set your Tesseract path
# Example (adjust if installed elsewhere):
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"Image file '{IMAGE_PATH}' not found!")

image = cv2.imread(IMAGE_PATH)
if image is None:
    raise ValueError("Could not load image")

# OCR with multiple languages (supports multilingual scripts)
print("🔍 Running OCR...")
extracted_text = pytesseract.image_to_string(image, lang=OCR_LANGS).strip()

if not extracted_text:
    print("❌ No text found in the image.")
    exit()

print(f"\n📝 Extracted Text:\n{extracted_text}")

# Translate using Google Translate (deep_translator)
print("\n🌐 Detecting and translating...")
translated = GoogleTranslator(source='auto', target=TARGET_LANG).translate(extracted_text)

print(f"\n🗣️ Translated Text ({TARGET_LANG}):\n{translated}")
