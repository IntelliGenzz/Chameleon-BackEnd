from pdf2image import convert_from_path
import os
import PyPDF2

def pdf_to_image(pdf_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(f"{output_path}/page_{i+1}.jpg", "JPEG")

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                text += page.extract_text()
            return text.strip()
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None