from django.contrib import admin
from .models import Numero, Cuentas_banco, Cliente, Comprobantes_de_pago, Vehiculo, ImagenSecundaria, Rifa
# Register your models here.

admin.site.register(Numero)
admin.site.register(Cliente)
admin.site.register(Comprobantes_de_pago)
admin.site.register(Cuentas_banco)
admin.site.register(Vehiculo)
admin.site.register(ImagenSecundaria)
admin.site.register(Rifa)