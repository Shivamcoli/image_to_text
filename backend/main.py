from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from utils import process_image
import os
import shutil
from uuid import uuid4

from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator
from typing import Dict
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# New endpoint: return supported languages
@app.get("/languages")
async def get_languages():
    translator = GoogleTranslator()
    return translator.get_supported_languages(as_dict=True)



UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/translate")
async def translate_image(file: UploadFile = File(...), target_lang: str = Form("en")):
    try:
        filename = f"{uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = process_image(file_path, target_lang)

        # Clean up
        os.remove(file_path)

        if result["error"]:
            return JSONResponse(status_code=400, content={"error": result["error"]})

        return {
            "extracted_text": result["extracted"],
            "translated_text": result["translated"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
