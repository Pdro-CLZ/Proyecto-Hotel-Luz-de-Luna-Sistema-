from django.db import models
from personal.models import Empleado, Rol

class UsuarioAdmin(models.Model):
    nombre_usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=100)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_usuario