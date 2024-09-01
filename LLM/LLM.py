import json
from Utils.body_builder import body_builder
from Utils.bucket_manipulation import bucket_contains_data,download_pdf_from_s3
from Utils.pdf_to_image import extract_text_from_pdf

async def ask_question_with_pdf(bedrock_client, question, pdf_text):
    try:
        userInput = f'Você é um copilot para bancos e fintechs, você deve ajudar a esclarecer dúvidas sobre o mercado financeiro para profissionais que estão chegando agora no mercado ou simplesmente não conhecem alguns termos ou procedimentos da empresa. Você receberá uma dúvida de um usuário e uma documentação para se embasar para responder uma dúvida dele. Caso o documento não possua uma resposta para a pergunta do usuário, use seus conhecimentos gerais para responder. Não fale ao cliente que você está usando documentos para se embasar, você é um copilot. \n Dificuldade do usuário: {question} \n  "Documento para se embasar: {pdf_text}'
        
        response = await body_builder(bedrock_client, userInput)
        response = json.loads(response['body'].read())
        response_final = response['content'][0]['text']
        return response_final
    except Exception as e:
        raise Exception(f"Erro ao invocar o modelo: {e}")

async def definirDoc(bedrock_client, question, filenames):
    try:
        userInput = f"""Você é auxiliar de sistema da Global Tech Solution que vai filtrar qual é o melhor documento para recomendar para um funcionário. Ele te enviará uma dúvida, você deve ler o nome das documentações existentes e recomendar a melhor para ele. \n Dificuldade do usuário: {question} \n  Documentos disponíveis: {filenames} \n você será utilizada em um sistema, então deve me retornar um json com o nome do documento que você considera o melhor para recomendar para o funcionário. Siga o modelo: "documento": "nome_do_documento.pdf". não coloque quebras de texto no json. Caso queira recomendar um documento do banco central, coloque "documento": "dadosBacen/" """
        
        response = await body_builder(bedrock_client, userInput)
        response = json.loads(response['body'].read())
        return response['content'][0]['text']
        
    except Exception as e:
        raise Exception(f"Erro ao invocar o modelo: {e}")

async def manage_bacen_data(s3_client, question):
    bucket_name = 'chameleon-hackathon-dev'
    response = await s3_client.list_objects_v2(Bucket=bucket_name, Prefix='dadosBacen/')
    if 'Contents' in response:
        filenames = [obj['Key'] for obj in response['Contents']]

        pdf_texts = []

        for filename in filenames:
            download_path = filename.split('/')[-1]
            await download_pdf_from_s3(bucket_name, filename, download_path)
            pdf_text = await extract_text_from_pdf(download_path)
            if pdf_text:
                pdf_texts.append(pdf_text)
            else:
                raise Exception(f"Erro ao extrair texto do PDF: {filename}")

        textao = ""
        for i, pdf_text in enumerate(pdf_texts):
            textao += f"PDF {i+1}:\n{pdf_text}\n"

    result = await ask_question_with_pdf(s3_client, question, textao)
    return result

async def ask_question(s3_client, bedrock_client, question):
    bucket_name = 'chameleon-hackathon-dev'

    filenames = await bucket_contains_data(bucket_name)
    object = json.loads(await definirDoc(bedrock_client, question, filenames))['documento']

    if object == 'dadosBacen/':
        return await manage_bacen_data(s3_client, question)
    else:
        await download_pdf_from_s3(bucket_name, object, 'arquivo.pdf')
        texto = extract_text_from_pdf('arquivo.pdf')
        result = await ask_question_with_pdf(bedrock_client, question, texto)
        return result
