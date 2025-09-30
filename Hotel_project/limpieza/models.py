from django.db import models
from personal.models import Empleado
from reservas.models import Habitacion, Estado

class TareaLimpieza(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.ImageField(upload_to="tareas/", blank=True, null=True)

    def __str__(self):
        return self.nombre


class Limpieza(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True) 
    observaciones = models.TextField(blank=True, null=True)
    tareas = models.ManyToManyField(TareaLimpieza, blank=True)

    def __str__(self):
        return f"Limpieza {self.habitacion} - {self.fecha}"

class Zona(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="zonas/")

    def __str__(self):
        return self.nombre

class TareaZona(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name="tareas")
    nombre = models.CharField(max_length=25)  
    foto = models.ImageField(upload_to="tareas/")

    def __str__(self):
        return f"{self.nombre} ({self.zona.nombre})"


