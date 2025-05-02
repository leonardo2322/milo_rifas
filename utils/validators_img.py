from django.core.exceptions import ValidationError
import os
from PIL import Image
import mimetypes

def validar_formato_imagen(imagen):
    ext_permitidas = ['JPEG', 'JPG', 'PNG', 'WEBP']
    mime_permitidos = ['image/jpeg', 'image/png', 'image/webp']
    max_size_kb = 2 * 1024 * 1024  # 500 KB

    with Image.open(imagen) as img:
        nombre_archivo = imagen.name.lower()
        _, extension = os.path.splitext(nombre_archivo)
        if extension not in ext_permitidas:
            raise ValidationError(f"Extensión de archivo no permitida: {extension}. Usa .jpeg, .jpg, .png o .webp.")
        formato = img.format
        mime_type, _ = mimetypes.guess_type(imagen.name)
        if mime_type not in mime_permitidos:
            raise ValidationError(f"Tipo de archivo no permitido: {mime_type}. Debe ser image/jpeg, image/png o image/webp.")
        if formato not in ext_permitidas:
            raise ValidationError(f"Formato no permitido: {formato}. Usa JPEG o PNG.")
        
        if imagen.size > max_size_kb:
            raise ValidationError(f"La imagen no puede pesar más de {max_size_kb} KB.")
        


    