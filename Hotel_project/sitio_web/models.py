from django.db import models
from administracion.models import Usuario, Rol
from personal.models import Direccion

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cliente')
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True, blank=True)

    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} ({self.usuario.username})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes" 
