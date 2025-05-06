from django.urls import path
from .views import Presentacion, ClienteFormView, SeleccionarNumeroView, SubirComprobanteView,VerificarNumerosDisponiblesView, Busqueda_cliente,liberar_reservas_cliente
from django.views.generic import TemplateView

urlpatterns = [
    path('', Presentacion.as_view(), name='inicio'),
    path('condiciones/',TemplateView.as_view(template_name='legal/disclaimer-rifas-milo.md'), name='condiciones'),
    path('politicas/',TemplateView.as_view(template_name='legal/politicas.html'), name='politicas'),
    path('terminos/',TemplateView.as_view(template_name='legal/term.html'), name='terminos'),
    path('verificar_numeros_disponibles/', VerificarNumerosDisponiblesView.as_view(), name='verificarnumeros'),
    path("liberar-reservas/", liberar_reservas_cliente, name="liberar_reservas"),
    path('cliente/', ClienteFormView.as_view(), name='cliente'),
    path('seleccionar_numero/', SeleccionarNumeroView.as_view(), name='seleccionar_numero'),
    path('comprobante/', SubirComprobanteView.as_view(), name='comprobante'),
    path('buscar_cliente/<str:dni>/', Busqueda_cliente.as_view(), name='busqueda'),


    # path('subir_comprobante/', SubirComprobanteView.as_view(), name='subir_comprobante'),

]
