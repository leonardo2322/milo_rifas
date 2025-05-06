from .models import PerfilUsuario, Vehiculo

def datos_globales(request):
    context = {}
    try:
        # Obtener el perfil del superusuario
        superuser_perfil = PerfilUsuario.objects.get(usuario__is_superuser=True)
        telefono_superuser = superuser_perfil.telefono
        correo = superuser_perfil.usuario.email
    except PerfilUsuario.DoesNotExist:
        telefono_superuser = None
        correo = None
    mensaje = "Hola, estoy interesado en comprar un boleto de la rifa. ¿Podrías ayudarme?;"

    # Obtener imágenes secundarias del primer vehículo si existe
    context['mensaje'] = mensaje
    context['usuario_tlfn'] = telefono_superuser
    context['correo'] = correo
    return context