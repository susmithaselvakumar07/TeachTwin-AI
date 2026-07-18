import os
from ai.pdf_reader import extract_pdf_text

print("Current Folder:", os.getcwd())
print("Files:", os.listdir())

pdf_path = "sample.pdf"

text = extract_pdf_text(pdf_path)

print(text)