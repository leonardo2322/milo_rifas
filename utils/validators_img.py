from django.core.exceptions import ValidationError

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