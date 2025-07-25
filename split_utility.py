import os
from PyPDF2 import PdfReader, PdfWriter
import math

def split_pdf(input_path, pages_per_file=30, output_dir="/tmp/splittedPDFs"):
    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(input_path)
    
    totalPagesNum = len(reader.pages)
    eachPDfSize = pages_per_file
    chunksNum = math.ceil(totalPagesNum / eachPDfSize)

    for i in range(chunksNum):
        writer = PdfWriter()
        start = i * eachPDfSize
        end = min(start + eachPDfSize, totalPagesNum)

        for page_num in range(start, end):
            writer.add_page(reader.pages[page_num])

        page_range_start = start + 1
        page_range_end = end
        file_name = f"pages_{page_range_start}-{page_range_end}.pdf"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "wb") as out_file:
            writer.write(out_file)

    print(f"Done splitting PDF into {chunksNum} files.")

