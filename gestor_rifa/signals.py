from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete,post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Cliente,PerfilUsuario # Ajusta si tu modelo está en otro lugar



@receiver(post_delete, sender=Cliente)
def eliminar_sesion_cliente(sender, instance, **kwargs):
    cliente_id_eliminado = instance.id
    sesiones = Session.objects.all()
    numeros_asociados = instance.numeros.all()
    for numero in numeros_asociados:
        numero.disponible = True
        numero.save()
    for sesion in sesiones:
        data = sesion.get_decoded()
        if data.get('cliente_id') == cliente_id_eliminado:
            sesion.delete()

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()