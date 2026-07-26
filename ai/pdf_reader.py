import fitz
import tempfile
import os


def extract_pdf_text(uploaded_file):

    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        temp_file_path = temp_file.name

    try:

        # Open the temporary PDF file
        pdf_document = fitz.open(
            temp_file_path
        )

        extracted_text = ""

        for page in pdf_document:
            extracted_text += page.get_text()

        pdf_document.close()

        return extracted_text

    finally:

        # Delete temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)