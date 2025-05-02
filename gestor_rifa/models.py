import io
import os
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil',blank=True, null=True)
    permisos_especiales = models.ManyToManyField('auth.Permission', blank=True)
    telefono = models.CharField(max_length=15, verbose_name='telefono',validators=[
            RegexValidator(
                regex=r'^\+?\d{1,3}?[ -]?\(?\d{1,4}?\)?[ -]?\d{1,4}[ -]?\d{1,4}$',  # Formato general
                message='Número de teléfono inválido. Ejemplo: +1 (234) 567-8901 o  234-567-8901  tambien (234) 567-8901',
                code='invalid_telefono'
            )
        ])
    def __str__(self):
        return f"Perfil de {self.usuario.username}"
# Create your models here.
class Numero(models.Model):
    numero = models.CharField(max_length=4, unique=True, validators=[
            RegexValidator(
                regex=r'^\d{3}$',
                message='Debe tener exactamente 3 dígitos (ej. 007, 123, 999)',
                code='invalid_numero'
            )
        ])
    disponible = models.BooleanField(verbose_name='disponibilidad',default=True)
    rifa = models.ForeignKey('Rifa', on_delete=models.CASCADE, related_name='numeros')
    fecha = models.DateField(auto_now_add=True)
    class Meta: 
        ordering = ['-numero']
    def __str__(self):
        if self.rifa:
            return f'Número: {self.numero} - Rifa: {self.rifa.nombre} - {'disponible'if self.disponible else 'ocupado'}'
        else:
            return f'numeros:{ self.numero} - sin rifa asignada - {'disponible'if self.disponible else 'ocupado'}'
    
    def liberar(self):
        """Marca el número como disponible y lo desvincula del cliente.
        """
        self.disponible = True
        self.cliente = None
        self.save()


class Rifa(models.Model):
    title = models.CharField(max_length=255, default='¡Tu oportunidad de Oro! Este espectacular carro puede ser tuyo.')
    nombre = models.CharField(max_length=255)
    fecha_sorteo = models.DateTimeField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    max_numeros = models.PositiveIntegerField(
        default=999,
        help_text="Número máximo permitido (ej. 999 ó 10000)"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Rifa: {self.nombre}'
    
class Vehiculo(models.Model):
    nombre = models.CharField(verbose_name="Nombre del vehiculo", max_length=50)
    ano = models.CharField(verbose_name="Año del vehiculo", max_length=4)
    marca = models.CharField(verbose_name="Marca del vehiculo", max_length=50)
    modelo = models.CharField(verbose_name="Modelo del vehiculo o descripcion", max_length=150, blank=True , null=True)
    img_p = models.ImageField(verbose_name="Imagen Principal", upload_to="principal/")
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE, related_name='premios',null=True)
    def __str__(self):
        return self.nombre

class ImagenSecundaria(models.Model):
    carro = models.ForeignKey(Vehiculo, related_name='imagenes_secundarias', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='carro/secundarias/')

    def __str__(self):
        return f"Imagen secundaria de {self.carro.nombre}"

class Cliente(models.Model):
    nombre = models.CharField(verbose_name='nombre',max_length=100)
    telefono = models.CharField(verbose_name='telefono',
        max_length=15,  # El tamaño máximo depende del formato que vayas a usar
        validators=[
            RegexValidator(
                regex=r'^\+?\d{1,3}?[ -]?\(?\d{1,4}?\)?[ -]?\d{1,4}[ -]?\d{1,4}$',  # Formato general
                message='Número de teléfono inválido. Ejemplo: +1 (234) 567-8901 o  234-567-8901  tambien (234) 567-8901',
                code='invalid_telefono'
            )
        ],
    )
    cedula = models.CharField(verbose_name='Cedula de identidad o dni puede llevar (. o , ej: 25.538.992)',max_length=12, unique=True,validators=[
            RegexValidator(
                regex=r'^\d{1,3}([.,]?\d{3}){2,3}$',  # Permite puntos o comas entre los números
                message='La cédula debe ser un número con 7 u 8 dígitos, opcionalmente con puntos o comas.',
                code='invalid_cedula'
            )
        ])
    estado = models.BooleanField(verbose_name='cliente activo o inactivo',default=False)
    direccion = models.CharField(verbose_name='direccion',max_length=255, blank=True, null=True)
    numeros = models.ManyToManyField(Numero, blank=True, related_name='clientes')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'cliente: {self.nombre} - numeros: {", ".join([str(numero.numero) for numero in self.numeros.all()]) if self.numeros.exists() else "sin numeros"} '
    def save(self, *args, **kwargs):
        # Eliminar puntos y comas antes de guardar
        if self.cedula:
            self.cedula = self.cedula.replace('.', '').replace(',', '')
        super().save(*args, **kwargs)

class Cuentas_banco(models.Model):
    nombre = models.CharField(verbose_name="nombre del banco",max_length=100, unique=True)
    titular = models.CharField(verbose_name="titular de la cuenta",max_length=100, blank=True, null=True)
    cedula = models.CharField(verbose_name="cedula de la cuenta",max_length=12, unique=True,validators=[
            RegexValidator(
                regex=r'^\d{1,3}([.,]?\d{3}){2,3}$',  # Permite puntos o comas entre los números
                message='La cédula debe ser un número con 7 u 8 dígitos, opcionalmente con puntos o comas.',
                code='invalid_cedula'
            )
        ],blank=True,
        null=True
        )
    tipo = models.CharField(verbose_name="tipo de cuenta",max_length=50, choices=[
        ('ahorros', 'Ahorros'),
        ('corriente', 'Corriente'),
    ], default='Corriente',
    blank=True,
    null=True
    )
    numero_cuenta = models.CharField(verbose_name="numero de cuenta",max_length=30, unique=True,
                                     validators=[
                RegexValidator(
                regex=r'^[\d\s\-]{20,30}$',
                message='El número de cuenta debe tener entre 20 y 30 caracteres, solo dígitos, espacios o guiones.',
                code='invalid_numero_cuenta'
        )],
        blank=True,
        null=True
        )
    telefono = models.CharField(verbose_name="telefono de la cuenta",
        max_length=15,  # El tamaño máximo depende del formato que vayas a usar
        validators=[
            RegexValidator(
                regex=r'^\+?\d{1,3}?[ -]?\(?\d{1,4}?\)?[ -]?\d{1,4}[ -]?\d{1,4}$',  # Formato general
                message='Número de teléfono inválido. Ejemplo: +1 (234) 567-8901 o  234-567-8901  tambien (234) 567-8901',
                code='invalid_telefono'
            )
        ],
        blank=True,  # Permitir que sea opcional
        null=True
    )
    correo = models.EmailField(
        unique=True,                
        max_length=254,             # Valor recomendado por la RFC
        verbose_name="Correo electrónico",
        blank=True,  # Permitir que sea opcional
        null=True
    )
    logo = models.ImageField(verbose_name="imagen de la cuenta", upload_to="iconos_bancos/")
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_actualizada = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Comprobantes_de_pago(models.Model):
    ESTADO_OPCIONES = [
        ('sin_pago', 'Sin comprobante'),
        ('pendiente', 'Pendiente de revisión'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    ultimos_digitos = models.CharField(verbose_name="digitos del comprobante de pago", max_length=4, unique=True, validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='Debe tener exactamente 4 dígitos (ej. 4444, 1234, 9999)',
                code='invalid_numero'
            )
        ])
    comprobante = models.ImageField(verbose_name="comprobante", upload_to="comprobantes/")
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='comprobantes')
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE, related_name='comprobantes',null=True,blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='sin_pago')
    def __str__(self):
        if self.cliente:
            return f"Comprobante de {self.cliente.nombre} - {self.ultimos_digitos} - identificacion {self.cliente.cedula}"
        else:
            return f'{self.ultimos_digitos} aun no asignado a un cliente'
