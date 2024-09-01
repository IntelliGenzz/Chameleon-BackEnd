from pdf2image import convert_from_path
from pdf2image import convert_from_path
import fitz

def pdf_to_image(pdf, output_path):
    images = convert_from_path(pdf)
    for i, image in enumerate(images):
        image.save(f"{output_path}/page_{i+1}.jpg", "JPEG")
    

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None
