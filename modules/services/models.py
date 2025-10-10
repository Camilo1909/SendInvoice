from django.conf import settings

import boto3
import requests


class WhatsAppService:

    @staticmethod
    def generate_presigned_url(file_path):
        """
        Genera una URL firmada válida por 10 minutos para el archivo en S3.
        """
        s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION_NAME,
        )

        try:
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": settings.AWS_STORAGE_BUCKET_NAME_MEDIA,
                    "Key": file_path,
                },
                ExpiresIn=600,  # 10 minutos
            )
            return url
        except Exception as e:
            print(f"[S3 Error] No se pudo generar URL firmada: {e}")
            return None

    @staticmethod
    def send_invoice(phone_number, image_url=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        }

        image_full_url = None
        if image_url:
            if image_url.startswith("http"):
                image_full_url = image_url
            else:
                # Generar URL firmada para S3
                image_full_url = WhatsAppService.generate_presigned_url(image_url)

        if not image_full_url:
            print("[Error] No se pudo generar la URL de imagen firmada")
            return False

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
                        "parameters": [{"type": "image", "image": {"link": image_full_url}}],
                    }
                ],
            },
        }

        response = requests.post(settings.WHATSAPP_API_URL, headers=headers, json=payload)
        print("HTTP status:", response.status_code)
        print("Response:", response.json())

        return response.status_code == 200
