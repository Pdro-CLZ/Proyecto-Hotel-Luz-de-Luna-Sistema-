# administracion/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Rol

User = get_user_model()

@receiver(post_migrate)
def crear_roles_y_admin(sender, **kwargs):
    if sender.name != "administracion":
        return

    # Crear rol Administrador
    rol_admin, _ = Rol.objects.get_or_create(nombre="Administrador")

    # Crear usuario administrador si no existe
    if not User.objects.filter(username="admin").exists():
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@hotel.com",
            password="admin1234"
        )
        admin.rol = rol_admin
        admin.save()

    # Crear otros roles
    otros_roles = ["Empleado Limpieza", "Manager", "Mantenimiento", "Cocina"]
    for nombre_rol in otros_roles:
        Rol.objects.get_or_create(nombre=nombre_rol)
