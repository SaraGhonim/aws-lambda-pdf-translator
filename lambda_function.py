import json 
import os
import tempfile
import boto3
from translation_process import translation_process  


s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
                 
        # Create temporary file paths
        with tempfile.TemporaryDirectory() as tmpdirname:
            input_file = os.path.join(tmpdirname, os.path.basename(key))

            # Download file from S3 source bucket
            s3_client.download_file(source_bucket, key, input_file)
                    
            # Process file based on extension
            ext = os.path.splitext(key)[1].lower()     
            if ext == ".pdf":
                print("Already a PDF")
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
            
            translation_process(input_file,tmpdirname,key)
            
            return {
                'statusCode': 200,
                'body': json.dumps(f"Successfully translated file: {key} ")
            }
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file: {str(e)}")
        }