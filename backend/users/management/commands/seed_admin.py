from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from users.models import Usuario
import os

class Command(BaseCommand):
    help = "Crea un usuario admin si no existe"

    def handle(self, *args, **options):
        email = os.environ.get("SEED_ADMIN_EMAIL")
        password = os.environ.get("SEED_ADMIN_PASSWORD")
        nombre = os.environ.get("SEED_ADMIN_NOMBRE", "Admin")
        apellido = os.environ.get("SEED_ADMIN_APELLIDO", "User")
        if not email or not password:
            self.stdout.write("SEED_ADMIN_EMAIL/PASSWORD no configurados, omitiendo seed")
            return
        try:
            user = Usuario.objects.get(email=email)
            self.stdout.write(f"Admin ya existe: {email}")
        except Usuario.DoesNotExist:
            user = Usuario(
                email=email,
                password_hash=make_password(password),
                nombre=nombre,
                apellido=apellido,
                rol="admin",
                activo=True,
                fecha_registro=timezone.now()
            )
            user.save(force_insert=True)
            self.stdout.write(f"Admin creado: {email}")
