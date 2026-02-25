import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

URL = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"


def enviar_whatsapp(numero: str, mensagem: str):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensagem}
    }

    response = requests.post(URL, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()