from django.urls import path
from .views import Presentacion, ClienteFormView, SeleccionarNumeroView, SubirComprobanteView
from django.views.generic import TemplateView

urlpatterns = [
    path('', Presentacion.as_view(), name='inicio'),
    path('condiciones/',TemplateView.as_view(template_name='legal/disclaimer-rifas-milo.md'), name='condiciones'),
    path('politicas/',TemplateView.as_view(template_name='legal/politicas.html'), name='politicas'),
    path('terminos/',TemplateView.as_view(template_name='legal/term.html'), name='terminos'),

    path('cliente/', ClienteFormView.as_view(), name='cliente'),
    path('seleccionar_numero/', SeleccionarNumeroView.as_view(), name='seleccionar_numero'),
    path('comprobante/', SubirComprobanteView.as_view(), name='comprobante'),

    # path('subir_comprobante/', SubirComprobanteView.as_view(), name='subir_comprobante'),

]
