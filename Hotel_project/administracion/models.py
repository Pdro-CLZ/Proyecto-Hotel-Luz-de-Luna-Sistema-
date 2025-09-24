from django.contrib.auth.models import AbstractUser
from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    cedula = models.CharField(max_length=9, unique=True)
    telefono = models.CharField(max_length=8)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"
