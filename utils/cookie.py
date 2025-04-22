from django.core.signing import Signer
from django.http import HttpResponse

signer = Signer()

def guardar_cookie(request):
    response = HttpResponse("Cookie creada")
    signed_id = signer.sign(participante.id)
    response.set_cookie("participante_token", signed_id, max_age=86400)  # 1 día
    return response

def obtener_participante(request):
    token = request.COOKIES.get("participante_token")
    if token:
        try:
            id = signer.unsign(token)
            participante = Participante.objects.get(id=id)
        except:
            participante = None