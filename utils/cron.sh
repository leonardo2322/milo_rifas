#!/bin/bash

# Activar el entorno virtual (ajusta esta ruta a tu entorno real)
source /ruta/a/tu/proyecto/venv/bin/activate

# Navegar a la carpeta del proyecto
cd /ruta/a/tu/proyecto

# Ejecutar el comando de Django
python manage.py limpiar_reservas_expiradas


crontab -e

*/10 * * * * /ruta/a/tu/proyecto/limpiar_reservas.sh >> /ruta/a/tu/proyecto/logs/limpieza_reservas.log 2>&1
