from django.urls import path
from .views import Presentacion
from django.views.generic import TemplateView

urlpatterns = [
    path('', Presentacion.as_view(), name='inicio'),
    path('condiciones/',TemplateView.as_view(template_name='legal/disclaimer-rifas-milo.md'), name='condiciones'),
    path('politicas/',TemplateView.as_view(template_name='legal/politicas.html'), name='politicas'),
    path('terminos/',TemplateView.as_view(template_name='legal/term.html'), name='terminos'),

]
