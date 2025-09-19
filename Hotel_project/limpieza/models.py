from django.db import models
from personal.models import Empleado
from reservas.models import Habitacion, Estado

class Limpieza(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha = models.DateField()
    observaciones = models.CharField(max_length=255)

    def __str__(self):
        return f"Limpieza {self.habitacion} - {self.fecha}"
