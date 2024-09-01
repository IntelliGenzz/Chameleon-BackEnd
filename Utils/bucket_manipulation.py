import aioboto3
from pdf2image import convert_from_path
import fitz
import os
from tempfile import NamedTemporaryFile

def pdf_to_image(pdf_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    images = convert_from_path(pdf_path)
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

async def bucket_contains_data(bucket_name):
    async with aioboto3.Session().client('s3', region_name='us-west-2') as s3_client:
        try:
            response = await s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                filenames = [obj['Key'] for obj in response['Contents']]
                return filenames
            else:
                return []
        except Exception as e:
            raise Exception(f"Erro ao listar objetos do bucket: {e}")

async def download_pdf_from_s3(bucket_name, object_key, download_path):
    async with aioboto3.Session().client('s3', region_name='us-west-2') as s3_client:
        try:
            await s3_client.download_file(bucket_name, object_key, download_path)
            print(f"Arquivo {object_key} baixado com sucesso do bucket {bucket_name}.")
        except Exception as e:
            raise Exception(f"Erro ao baixar o arquivo do S3: {e}")

async def upload_to_s3(bucket_name, file_path):
    async with aioboto3.Session().client('s3', region_name='us-west-2') as s3_client:
        try:
            await s3_client.upload_file(file_path, bucket_name, os.path.basename(file_path))
            print(f"Arquivo {file_path} enviado com sucesso para o bucket {bucket_name}.")
        except Exception as e:
            raise Exception(f"Erro ao enviar o arquivo para o S3: {e}")

async def upload_txt_to_s3(file):
    file_name = f"{file.filename[:10]}.txt"
    try:
        with NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(file.file.read())
            tmp_file.flush()
            tmp_file_name = os.path.basename(tmp_file.name)
        
        async with aioboto3.Session().client('s3', region_name='us-west-2') as s3_client:
            await s3_client.upload_file(tmp_file.name, "chameleon-hackathon-dev", tmp_file_name)
        
        print(f"Arquivo de texto {tmp_file_name} enviado com sucesso para o bucket chameleon-hackathon-dev.")
    except Exception as e:
        raise Exception(f"Erro ao enviar o arquivo de texto para o S3: {e}")
    finally:
        os.remove(tmp_file.name)
