import requests

from core.config import (
    AUTHENTICATION_API_KEY,
    EVOLUTION_INSTANCE_NAME,
    EVOLUTION_API_URL
)


def send_whatsapp_message(number, text):
    url = f'{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE_NAME}'
    headers = {
        'apiKey': AUTHENTICATION_API_KEY,
        'Content-Type': 'application/json'
    }
    body = {
        'number': number,
        'text': text
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=body
    )
    response.raise_for_status()

    return response
