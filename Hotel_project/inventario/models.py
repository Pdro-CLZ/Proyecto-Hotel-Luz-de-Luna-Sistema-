from django.db import models
from reservas.models import Estado

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre_item = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)  # redundante pero estaba en tu script
    cantidad = models.IntegerField()
    unidad = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()

    def __str__(self):
        return f"{self.nombre_item} ({self.cantidad} {self.unidad})"
