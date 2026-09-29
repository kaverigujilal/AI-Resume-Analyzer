import fitz


def extract_text_from_pdf(uploaded_file):

    pdf_bytes = uploaded_file.read()

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text