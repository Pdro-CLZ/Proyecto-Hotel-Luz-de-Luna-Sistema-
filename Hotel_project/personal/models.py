from django.utils import timezone
from django.db import models
from administracion.models import Rol, Usuario

class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Canton(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Distrito(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Direccion(models.Model):
    direccion_exacta = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)

    def __str__(self):
        return self.direccion_exacta


class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT, null=True, blank=True)  
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    

class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now) 
    hora_llegada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    horas_trabajadas = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    observaciones = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('empleado', 'fecha')

    def __str__(self):
        return f"Asistencia {self.empleado} - {self.fecha}"
