import google.generativeai as genai
from save_translation import save_translation
import os
import time
import random

API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

def call_gemini(fileToTranslate ,retries=3, delay=5):
    with open(fileToTranslate, "rb") as f:
         file_bytes = f.read()
    for attempt in range(retries):
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
            if attempt < retries - 1:
                wait_time = delay + random.uniform(0, 3)
                print(f"Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Max retries reached for {fileToTranslate}")
                with open("errors.log", "a", encoding="utf-8") as log:
                    log.write(f"{fileToTranslate} failed: {str(e)}\n")
                return None

  