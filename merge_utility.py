
import os
from natsort import natsorted
import sys
import boto3
import io

s3_client = boto3.client('s3')

OUTPUT_BUCKET = 'translateddocs0120'
file_type = 'txt'

def merge_translations(input_folder, output_folder):
    full_text=""
      
    os.makedirs(output_folder, exist_ok=True)
    files = natsorted([f for f in os.listdir(input_folder) ])

    for filename in files:
        # Save as txt
        print(filename)
        txt_path = os.path.join(input_folder, f"{filename}")
        with open(txt_path, "r", encoding="utf-8") as f:
            full_text+= f.read()

    # Save as txt
    print("Saving to: ", output_folder)
    with open(os.path.join(output_folder, "Translated_PDF.txt"), "w", encoding="utf-8") as f:
        f.write(full_text)

    # s3_client.put_object(
    #     Bucket=OUTPUT_BUCKET,
    #     Key="Translated_PDF.txt",
    #     Body=full_text.encode('utf-8'),
    #     ContentType='text/plain'
    # )
          
