from django.db import IntegrityError
from UI_milo.models import Numero

def crear_numeros():
    for i in range(1000):  # Desde 0 hasta 999
        numero = str(i).zfill(3)  # Convertir el número a cadena con 3 dígitos, ej: 000, 001, ..., 999

        try:
            # Crear el número en la base de datos
            Numero.objects.create(numero=numero)
            print(f"Creado número: {numero}")
        except IntegrityError:
            # Si el número ya existe, ignorar el error
            print(f"El número {numero} ya existe.")