import json

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Para recibir notificaciones de WhatsApp, deshabilitamos CSRF
@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":

        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("Forbidden", status=403)

    elif request.method == "POST":
        # WhatsApp envía JSON con los mensajes
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Bad Request", status=400)

        print("Webhook payload:", json.dumps(payload, indent=2))

        return JsonResponse({"status": "received"}, status=200)

    return HttpResponse("Method not allowed", status=405)
