import google.generativeai as genai
# from google import genai
# from google.genai import types
from save_translation import save_translation
import os
import time
import random

API_KEY = "AIzaSyCpPrWdbnaRhsBWczNb0pzeNbCfiMgPoaw"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')


def call_gemini_pdf(fileToTranslate):
    with open(fileToTranslate, "rb") as f:
         file_bytes = f.read()

    try:
        
        response = model.generate_content(

            contents=[
{
    "inline_data": {
        "mime_type": "application/pdf",
        "data": file_bytes  # raw bytes
    }
},
{
    "text": "Translate the contents of this PDF into Arabic.Maintain the original formatting, headings, bullet points, and structure as much as possible. Return only the translation with the page number صفحة, with no additions, explanations, or suggestions"           
}
]
        )
        print(response.text)
        return response.text
    except Exception as e:
        print(f"Error while translating {fileToTranslate}: {e}")


def is_corrupted(path, min_length=100):
    if not os.path.exists(path):
        return True
  
def translate_pdfs(pdfs_folder,translation_folder):
    for filename in sorted(os.listdir(pdfs_folder)):
        if not filename.lower().endswith(".pdf"):
            continue

        txt_filename = filename.replace(".pdf", ".txt")
        output_path = os.path.join(translation_folder, txt_filename)

        if not is_corrupted(output_path):
            print(f"Skipping already translated and valid: {filename}")
            continue

        print(f"Translating or re-translating: {filename}")
        file_path = os.path.join(pdfs_folder, filename)
        translated = call_gemini_pdf(file_path)
        if translated:
            save_translation(txt_filename, translated,translation_folder)
