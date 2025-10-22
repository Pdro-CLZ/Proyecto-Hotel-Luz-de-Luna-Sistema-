from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    cedula = models.CharField(max_length=9, unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"
    
class PasswordResetToken(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    expira = models.DateTimeField()
    usado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.token[:10]}..."

    @classmethod
    def crear_token(cls, usuario, minutos_validos=10):
        """Crea un token único de un solo uso, válido por `minutos_validos` minutos."""
        token = secrets.token_urlsafe(32)
        expira = timezone.now() + timedelta(minutes=minutos_validos)
        token_obj = cls.objects.create(usuario=usuario, token=token, expira=expira)
        return token_obj
