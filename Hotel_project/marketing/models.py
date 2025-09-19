from django.db import models
from reservas.models import Estado

class CampaniaMarketing(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    canal = models.CharField(max_length=50)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
