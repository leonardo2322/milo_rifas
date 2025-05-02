from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect,render
from django.contrib import messages

from .models import Numero, Cuentas_banco, Cliente, Comprobantes_de_pago, Vehiculo, ImagenSecundaria, Rifa,PerfilUsuario
from .forms import SeleccionRifaForm
from utils.creacion_numeros import crear_numeros
# Register your models here.


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

admin.site.register(Numero, NumeroAdmin)
admin.site.register(PerfilUsuario)
admin.site.register(Cliente)
admin.site.register(Comprobantes_de_pago)
admin.site.register(Cuentas_banco)
admin.site.register(Vehiculo)
admin.site.register(ImagenSecundaria)
admin.site.register(Rifa)