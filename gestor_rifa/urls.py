from django.urls import path
from .views import Presentacion


urlpatterns = [
    path('', Presentacion.as_view(), name='inicio'),
]
