from django.core.management.base import BaseCommand
from django.utils import timezone
from .models import ReservaTemporal  # Ajusta el import a tu app

class Command(BaseCommand):
    help = 'Elimina todas las reservas temporales que ya expiraron'

    def handle(self, *args, **kwargs):
        expiradas = ReservaTemporal.objects.filter(expiracion__lt=timezone.now())
        total = expiradas.count()
        expiradas.delete()
        self.stdout.write(self.style.SUCCESS(f'{total} reservas expiradas eliminadas correctamente.'))
