from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from os import environ
import boto3
from Utils.pdf_to_image import pdf_to_image
from Utils.voice_recognition import speech_to_text
from Utils.bucket_manipulation import upload_txt_to_s3, upload_to_s3
from LLM.LLM import ask_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

aws_region = "us-west-2"

session = boto3.Session(
    aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=aws_region
)

s3_client = session.client('s3')
bedrock_client = session.client('bedrock-runtime', region_name=aws_region)

@app.get("/generate-response")
async def generate_response(userInput: str, is_audio_file: bool = False):
    try:
        userInput = str(userInput)
        print(f"User input: {userInput}")
        if is_audio_file:
            userInput = speech_to_text(userInput)
        
        result = await ask_question(s3_client, bedrock_client, userInput)
        return {"response": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-train-files")
async def send_train_files(file: bytes, file_type: str):
    try:
        if file_type == "text":
            await upload_txt_to_s3(s3_client, file)
            
        elif file_type == "audio":
            file_text = speech_to_text(file)
            await upload_txt_to_s3(s3_client, file_text)
            
        elif file_type == "image":
            await upload_to_s3(s3_client, "chameleon-hackathon-dev", file)
            
        elif file_type == "pdf":
            pdf_to_image(file, "images")
        
        return {"message": "File processed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
