from django.db import models

class Contabilidad(models.Model):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto'),
    ]

    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    metodo_pago = models.CharField(max_length=20, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tipo} - {self.monto}"


class CierreMensual(models.Model):
    mes = models.IntegerField()
    anio = models.IntegerField()
    total_ingresos = models.DecimalField(max_digits=12, decimal_places=2)
    total_gastos = models.DecimalField(max_digits=12, decimal_places=2)
    utilidad = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_cierre = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cierre {self.mes}/{self.anio}"


class CierreAnual(models.Model):
    anio = models.IntegerField()
    total_ingresos = models.DecimalField(max_digits=12, decimal_places=2)
    total_gastos = models.DecimalField(max_digits=12, decimal_places=2)
    utilidad = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_cierre = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cierre Anual {self.anio}"
