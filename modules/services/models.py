# from django.db import models
from django.conf import settings

import requests

# Create your models here.


class WhatsAppService:

    @staticmethod
    def send_invoice(phone_number, image_url=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": f"+57{phone_number}",
            "type": "template",
            "template": {
                "name": "send_invoice",
                "language": {"code": "es_CO"},
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "image",
                                "image": {
                                    "link": f"https://glady-nonremedial-alda.ngrok-free.dev/{image_url}"
                                },
                            }
                        ],
                    }
                ],
            },
        }
        response = requests.post(settings.WHATSAPP_API_URL, headers=headers, json=payload)
        # Depuración
        print("HTTP status:", response.status_code)
        print("Response:", response.json())

        # Retornar True solo si no hay error en la API
        resp_json = response.json()
        if response.status_code == 200 and "error" not in resp_json:
            return True
        else:
            print("Error enviando WhatsApp:", resp_json.get("error"))
            return False
