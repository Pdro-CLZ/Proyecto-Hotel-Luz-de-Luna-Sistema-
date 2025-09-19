from django.db import models

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


class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
