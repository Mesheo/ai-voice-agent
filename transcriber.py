from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(filename):
    try:
        with open(filename, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe", 
                file=audio_file, 
                response_format="text",
                language="pt"
            )            
            return transcription
        
    except Exception as e:
        print("Erro ao transcrever o áudio:", e)
        return ""
