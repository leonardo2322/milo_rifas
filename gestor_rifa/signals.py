import os
from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete,post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Cliente,PerfilUsuario,Vehiculo,Numero,Comprobantes_de_pago # Ajusta si tu modelo está en otro lugar



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
    Comprobantes_de_pago.objects.filter(cliente=instance).delete()

@receiver(post_delete, sender=Vehiculo)
def eliminar_vehiculo(sender, instance, **kwargs):
    # Eliminar imagen principal si existe
    if instance.img_p and os.path.isfile(instance.img_p.path):
        os.remove(instance.img_p.path)

    # Eliminar imágenes secundarias y sus archivos
    for img_sec in instance.imagenes_secundarias.all():
        if img_sec.imagen and os.path.isfile(img_sec.imagen.path):
            os.remove(img_sec.imagen.path)
        img_sec.delete()


@receiver(post_delete, sender=Comprobantes_de_pago)
def eliminar_comprobantes(sender, instance, **kwargs):
    # Aquí eliminamos los números relacionados al cliente eliminado
    if instance.cliente:
        Numero.objects.filter(clientes=instance.cliente, disponible=False).update(disponible=True)
        if instance.comprobante and os.path.isfile(instance.comprobante.path):
            os.remove(instance.comprobante.path)
        # Eliminar al cliente
        instance.cliente.delete()

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()