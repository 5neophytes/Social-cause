import fitz 


def extract_pdf(filepath):
    doc = fitz.open(filepath)


    extracted_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        extracted_text += page.get_text()

    return extracted_text

