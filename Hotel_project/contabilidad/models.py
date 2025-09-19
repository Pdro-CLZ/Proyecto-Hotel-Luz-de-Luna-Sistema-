from django.db import models
from reservas.models import Reserva

class Contabilidad(models.Model):
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  # Ingreso / Gasto
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.monto}"
