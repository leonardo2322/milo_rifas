import json
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect,render
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Numero, Cuentas_banco, Cliente, Comprobantes_de_pago, Vehiculo, ImagenSecundaria, Rifa,PerfilUsuario
from .forms import SeleccionRifaForm
from utils.creacion_numeros import crear_numeros
# Register your models here.
from django.utils.html import format_html


class NumeroAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('crear-numeros/', self.admin_site.admin_view(self.crear_numeros), name='crear_numeros'),
        ]
        return custom_urls + urls

    def crear_numeros(self, request):
        if not request.user.is_superuser:
            self.message_user(request, "No tienes permiso para realizar esta acción.", level=messages.ERROR)
            return redirect('..')

        if request.method == 'POST':
            form = SeleccionRifaForm(request.POST)
            if form.is_valid():
                rifa = form.cleaned_data['rifa']

                # Verifica si ya existen números para esta rifa
                if Numero.objects.filter(rifa=rifa.pk).exists():
                    self.message_user(request, f"Ya existen números para la rifa .", level=messages.WARNING)
                else:
                    crear_numeros(rifa_nombre=rifa, max_numeros=rifa.max_numeros)
                    self.message_user(request, f"Números creados para la rifa .", level=messages.SUCCESS)
                return redirect('..')
        else:
            form = SeleccionRifaForm()

        context = {
            'form': form,
            'title': 'Crear Números por Rifa',
        }
        return render(request, 'admin/crear_numeros.html', context)

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['extra_button'] = True
        return super().changelist_view(request, extra_context)


class ComprobantesDePagoAdmin(admin.ModelAdmin):
    list_display = ['ultimos_digitos', 'mostrar_imagen_con_url', 'fecha', 'cliente_nombre', 'rifa_nombre', 'estado']
    readonly_fields = ['mostrar_imagen_con_url', 'fecha', 'cliente', 'rifa'] # Hacer estos campos solo lectura en la edición

    def mostrar_imagen_con_url(self, obj):
        if obj.comprobante:
            return mark_safe(f'<p>URL: <a href="{obj.comprobante.url}" target="_blank">{obj.comprobante.url}</a></p>'
                             f'<img src="{obj.comprobante.url}" alt="{obj.comprobante.name}" style="max-height: 200px; max-width: 200px;">')
        else:
            return "Sin comprobante"
    mostrar_imagen_con_url.short_description = 'Comprobante'

    def cliente_nombre(self, obj):
        return obj.cliente.nombre if obj.cliente else "Sin cliente"
    cliente_nombre.short_description = 'Cliente'
    cliente_nombre.admin_order_field = 'cliente__nombre' # Permite ordenar por el nombre del cliente

    def rifa_nombre(self, obj):
        return obj.rifa.nombre if obj.rifa else "Sin rifa"
    rifa_nombre.short_description = 'Rifa'
    rifa_nombre.admin_order_field = 'rifa__nombre' # Permite ordenar por el nombre de la rifa


from django.utils.html import format_html

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'telefono', 'estado', 'generar_factura_button')
    readonly_fields = ('generar_factura_button',)

    def generar_factura_button(self, obj):
        if obj and obj.pk:
            tiene_comprobante_aprobado = obj.comprobantes.filter(estado='aprobado').exists()
            if tiene_comprobante_aprobado:
                try:
                    rifa_activa = Rifa.objects.filter(activa=True).first()
                    vehiculo_activo = rifa_activa.premios.first() if rifa_activa else None
                    logo_url = vehiculo_activo.img_p.url if vehiculo_activo and vehiculo_activo.img_p else staticfiles_storage.url('img/vehiculos/carro.webp')
                except:
                    logo_url = staticfiles_storage.url('img/vehiculos/carro.webp')

                return format_html(
                    '<button class="descargar-factura" '
                    'data-imagen="{}" data-cliente="Estimado cliente: {}" data-descripcion="Sus numeros seleccionados: {} con los que participara en la rifa ">'
                    'Descargar Factura</button>',
                    logo_url,
                    obj.nombre,
                    ', '.join(str(num.numero) for num in obj.numeros.all())
                )
        return "aprobar comprobante del cliente para generar la factura"
    generar_factura_button.short_description = 'Generar Lista de Números'


admin.site.register(Comprobantes_de_pago, ComprobantesDePagoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Numero, NumeroAdmin)
admin.site.register(PerfilUsuario)
admin.site.register(Cuentas_banco)
admin.site.register(Vehiculo)
admin.site.register(ImagenSecundaria)
admin.site.register(Rifa)