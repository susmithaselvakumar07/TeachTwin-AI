import fitz


def extract_pdf_text(uploaded_file):

    # Read the uploaded PDF directly from memory
    pdf_bytes = uploaded_file.getvalue()

    # Open PDF from memory
    pdf_document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    extracted_text = ""

    for page in pdf_document:
        extracted_text += page.get_text()

    pdf_document.close()

    return extracted_text