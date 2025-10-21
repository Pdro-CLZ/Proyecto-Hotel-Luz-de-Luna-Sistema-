from django.db import models
from django.utils import timezone
from administracion.models import Usuario

class ZonaLimpieza(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='zonas_limpieza/', null=True, blank=True)
    detalles = models.TextField(null=True, blank=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='zonas_registradas')
    estado = models.CharField(max_length=50, default='No disponible')
    fecha_registro = models.DateTimeField(default=timezone.now)
    is_habitacion = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class TareaLimpieza(models.Model):
    zona = models.ForeignKey(ZonaLimpieza, on_delete=models.CASCADE, related_name='tareas')
    nombre = models.CharField(max_length=100)
    detalles = models.TextField(null=True, blank=True)
    foto = models.ImageField(upload_to='tareas_limpieza/', null=True, blank=True)
    estado = models.CharField(max_length=50, default='Pendiente')
    observaciones_empleado = models.TextField(blank=True, null=True)
    usuario_modifica = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='tareas_modificadas', null=True, blank=True)
    fecha_modificacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} - {self.zona.nombre}"
