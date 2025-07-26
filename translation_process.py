import boto3
import os
from split_utility import split_pdf
from translate_pdfs import translate_pdfs
from merge_utility import merge_translations

s3_client = boto3.client('s3')
dest_bucket = os.environ["DEST_BUCKET_NAME"]

def translation_process(input_file,tmpdirname,key):            
        # Main processing logic
        print("Step 1: Splitting PDF...")
        output_dir = os.path.join(tmpdirname, "Splitted_PDFs")
        split_pdf(input_file, output_dir=output_dir)

            
        print("Step 2: Translating Splitted PDFs one by one...")
        translation_folder = os.path.join(tmpdirname, "Translated_PDFs")
        translate_pdfs(output_dir,translation_folder)
        
        print("Step 3: Merging translated PDFs...")
        output_prefix = os.path.join(tmpdirname, "Merged_PDFs")
        merge_translations(translation_folder, output_prefix)
        
        # Upload results back to S3 
        output_key = f"translated/{os.path.splitext(key)[0]}.txt"
        output_file =  os.path.join(output_prefix,"Translated_PDF.txt" )
        if os.path.exists(output_file):
            print(f"Uploading result to S3: {output_key}")
            s3_client.upload_file(output_file, dest_bucket, output_key)
        else:
            raise FileNotFoundError(f"Output file {output_file} not found")
        