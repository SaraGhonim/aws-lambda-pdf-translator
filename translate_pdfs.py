import os
from save_translation import save_translation
from call_gemini import call_gemini

def translate_pdfs(pdfs_folder,translation_folder):
    os.makedirs(translation_folder, exist_ok=True)  
    for filename in  os.listdir(pdfs_folder):
        
        txt_filename = filename.replace(".pdf", ".txt")
        file_path = os.path.join(pdfs_folder, filename)
        translated = call_gemini(file_path)
        if translated:
            save_translation(txt_filename, translated,translation_folder)
