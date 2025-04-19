from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_gpt_response(transcribed_text):
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "system",
                    "content": "Você é um atendente educado e motivado a ajudar. Seja solícito e tente sempre entender a dor do cliente que te mandou a mensagem"
                },
                {
                    "role": "user",
                    "content": transcribed_text
                }
            ]
        )
        print(response.output_text)

    except Exception as e:
        print("Erro ao obter resposta do GPT-4:", e)
        return ""




