from django.views.generic import ListView
from .models import Vehiculo


class Presentacion(ListView):
    model = Vehiculo
    template_name = 'vehiculo/vehiculo.html'
    context_object_name = 'vehiculos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imagenes = Vehiculo.objects.first().imagenes_secundarias.all()
        context['imagenes'] = imagenes
        return context

