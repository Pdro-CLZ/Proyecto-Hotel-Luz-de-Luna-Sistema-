from django.db import models
from administracion.models import Usuario

class Reporte(models.Model):
    tipo_reporte = models.CharField(max_length=50)
    fecha_generacion = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    detalle = models.TextField()

    def __str__(self):
        return f"{self.tipo_reporte} - {self.fecha_generacion}"
