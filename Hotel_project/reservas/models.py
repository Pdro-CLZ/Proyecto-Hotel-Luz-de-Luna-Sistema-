from django.db import models


class Amenidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    amenidades = models.ManyToManyField(Amenidad, related_name='habitaciones')

    def __str__(self):
        return self.nombre


class PrecioHabitacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='precios')
    fecha = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('habitacion', 'fecha')
        indexes = [
            models.Index(fields=['habitacion', 'fecha']),
        ]
        verbose_name_plural = 'Precios de Habitaciones'

    def __str__(self):
        return f"{self.habitacion.nombre} - {self.fecha}: ₡{self.precio}"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Reserva(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='reservas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['habitacion', 'fecha_inicio', 'fecha_fin']),
            models.Index(fields=['cliente']),
        ]

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente} ({self.habitacion.nombre})"


class FechaReservada(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='fechas_reservadas')
    fecha = models.DateField()
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='fechas_reservadas')

    class Meta:
        unique_together = ('habitacion', 'fecha')
        indexes = [
            models.Index(fields=['habitacion', 'fecha']),
        ]
        verbose_name_plural = 'Fechas Reservadas'

    def __str__(self):
        return f"{self.habitacion.nombre} - {self.fecha}"
