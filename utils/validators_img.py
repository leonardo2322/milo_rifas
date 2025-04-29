from django.core.exceptions import ValidationError
import os
from PIL import Image

def validar_formato_imagen(imagen):
    from PIL import Image
    ext_permitidas = ['JPEG', 'JPG', 'PNG', 'WEBP']
    max_size_kb = 2 * 1024 * 1024  # 500 KB

    with Image.open(imagen) as img:
        formato = img.format
        if formato not in ext_permitidas:
            raise ValidationError(f"Formato no permitido: {formato}. Usa JPEG o PNG.")
        
        if imagen.size > max_size_kb:
            raise ValidationError(f"La imagen no puede pesar más de {max_size_kb} KB.")
        

def redimensionar_y_recortar(imagen_path, salida_path, tamaño=(500, 500)):
    imagen = Image.open(imagen_path)
    imagen = imagen.convert("RGB")  # convierte a RGB si es webp o tiene canal alpha
    
    # Escalar manteniendo proporción
    imagen.thumbnail((max(tamaño), max(tamaño)))

    # Crear fondo blanco 500x500
    fondo = Image.new("RGB", tamaño, (255, 255, 255))
    x = (tamaño[0] - imagen.width) // 2
    y = (tamaño[1] - imagen.height) // 2
    fondo.paste(imagen, (x, y))

    fondo.save(salida_path, quality=95)
    
# Ejemplo:
redimensionar_y_recortar(r"C:\Users\leonardo\Desktop\milo\milo_rifas\utils\m5.jpg", "m2.jpg")
def marcar_numero_seleccionado(self, numero_id, channel_name, cliente):
        try:
            numero = Numero.objects.get(pk=numero_id, disponible=True)
            numero.disponible = False
            numero.seleccionado_por_canal = channel_name
            numero.cliente = cliente # Asocia el cliente al número
            numero.save()