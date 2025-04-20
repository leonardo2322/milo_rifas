from django.urls import path,include
from .views import Presentacion
urlpatterns = [
    path('', Presentacion.as_view(), name='inicio'),
]