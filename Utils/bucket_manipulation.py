from os import remove

async def bucket_contains_data(s3_client, bucket_name: str) -> list:
    response = await s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        filenames = [obj['Key'] for obj in response['Contents']]
        return filenames
    else:
        raise Exception("Nenhum arquivo encontrado no bucket.")

async def download_pdf_from_s3(s3_client, bucket_name: str, object_key: str, download_path: str) -> None:
    try:
        await s3_client.download_file(bucket_name, object_key, download_path)
        print(f"Arquivo {object_key} baixado com sucesso do bucket {bucket_name}.")
    except Exception as e:
        raise Exception(f"Erro ao baixar o arquivo do S3: {e}")

async def upload_to_s3(s3_client, bucket_name: str, file_path: str) -> None:
    try:
        await s3_client.upload_file(file_path, bucket_name, file_path.split('/')[-1])
        print(f"Arquivo {file_path} enviado com sucesso para o bucket {bucket_name}.")
    except Exception as e:
        raise Exception(f"Erro ao enviar o arquivo para o S3: {e}")

async def upload_txt_to_s3(s3_client, file) -> None:
    file_name = f"{file.filename[:10]}.txt"
    try:
        with open(file_name, "w") as txt_file:
            txt_file.write(file.filename)

        await s3_client.upload_file(file_name, "chameleon-hackathon-dev", file_name)
        await s3_client.put_object(Body=file, Bucket="chameleon-hackathon-dev", Key=file_name)
    except Exception as e:
        raise Exception(f"Erro ao enviar o arquivo de texto para o S3: {e}")
    finally:
        remove(file_name)
