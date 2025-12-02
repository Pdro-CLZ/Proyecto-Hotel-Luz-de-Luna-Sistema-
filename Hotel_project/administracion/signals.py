# administracion/signals.py

from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Rol
from marketing.models import ContactoMarketing

User = get_user_model()

# --- Señal para crear roles y admin al migrar ---
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
    otros_roles = ["Empleado_Nivel1", "Empleado_Nivel2", "Cliente"]
    for nombre_rol in otros_roles:
        Rol.objects.get_or_create(nombre=nombre_rol, activo=True)


# --- Señal para crear ContactoMarketing al crear usuario Cliente ---
@receiver(post_save, sender=User)
def crear_contacto_marketing(sender, instance, created, **kwargs):
    if created and instance.rol and instance.rol.nombre == "Cliente":
        # Crear contacto si no existe
        ContactoMarketing.objects.get_or_create(
            nombre=instance.first_name if hasattr(instance, "first_name") else instance.username,
            apellido=instance.last_name if hasattr(instance, "last_name") else "",
            correo=instance.email
        )
