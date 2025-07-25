import json
import boto3
import os
import tempfile
import urllib.parse
   
from split_utility import split_pdf
from translate_pdfs import translate_pdfs
from  merge_utility import merge_translations
s3_client = boto3.client('s3')

OUTPUT_BUCKET = 'translateddocs0120'

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
                 
        # Create temporary file paths
        with tempfile.TemporaryDirectory() as tmpdirname:
            input_file = os.path.join(tmpdirname, os.path.basename(key))
            output_pdf = os.path.splitext(input_file)[0] + ".pdf"
            
            # Download file from S3
            print(f"Downloading {key} from S3 bucket {bucket}...")
            s3_client.download_file(bucket, key, input_file)
                    
            # Process file based on extension
            ext = os.path.splitext(key)[1].lower()
                
            if ext == ".pdf":
                print("Already a PDF")
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
            
            # Main processing logic
            output_dir = os.path.join(tmpdirname, "splittedPDFs")
            
            print("Step 1: Splitting PDF...")
            split_pdf(input_file, output_dir=output_dir)

             
            print("Step 2: Translating Splitted PDFs one by one...")
            translation_folder = os.path.join(tmpdirname, "translationResult")
            os.makedirs(translation_folder, exist_ok=True)  
            translate_pdfs(output_dir,translation_folder)
            
            # Adjust folder paths for Lambda's tmp directory
  
            print("Step 3: Merging translated Splitted PDFs...")
            output_prefix = os.path.join(tmpdirname, "merged_files")
            os.makedirs(output_prefix, exist_ok=True)  
            
            merge_translations(translation_folder, output_prefix)
            
            # Upload results back to S3 (assuming merge_translations creates a file)
            output_key = f"translated/{os.path.splitext(key)[0]}.txt"
            output_file =  os.path.join(output_prefix,"Translated_PDF.txt" )
           
            #  f"{output_prefix}.txt"  # Adjust based on your merge_translations output
            if os.path.exists(output_file):
                print(f"Uploading result to S3: {output_key}")
                s3_client.upload_file(output_file, OUTPUT_BUCKET, output_key)
            else:
                raise FileNotFoundError(f"Output file {output_file} not found")
            
            return {
                'statusCode': 200,
                'body': json.dumps(f"Successfully processed {key} and uploaded to {output_key}")
            }
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file: {str(e)}")
        }