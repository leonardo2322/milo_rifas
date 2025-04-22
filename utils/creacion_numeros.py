
from django.db import IntegrityError
from gestor_rifa.models import Numero

def crear_numeros(rifa_nombre, max_numeros=1000):
    """
    Crea números del 000 al max_numeros - 1 asociados al nombre de una rifa.
    """


    for i in range(max_numeros):
        numero = str(i).zfill(len(str(max_numeros - 1)))  # ej: 000, 001 ... 9999
        try:
            Numero.objects.create(numero=numero, rifa=rifa_nombre)
        except IntegrityError:
            print(f"El número {numero} ya existe. Verifica la base de datos.")