
import os
from natsort import natsorted

def merge_translations(input_folder, output_folder):
    full_text=""
      
    os.makedirs(output_folder, exist_ok=True)
    files = natsorted([f for f in os.listdir(input_folder) ])

    for filename in files:
        txt_path = os.path.join(input_folder, f"{filename}")
        with open(txt_path, "r", encoding="utf-8") as f:
            full_text+= f.read()

    with open(os.path.join(output_folder, "Translated_PDF.txt"), "w", encoding="utf-8") as f:
        f.write(full_text)
