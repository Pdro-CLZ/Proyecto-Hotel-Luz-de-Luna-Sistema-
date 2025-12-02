from django.db import models
from sitio_web.models import Cliente


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


class Reserva(models.Model):
    METODOS_PAGO = [
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('sitio', 'Sitio'),
    ]

    CANALES_RESERVACION = [
        ('sitio', 'Sitio'),
        ('directo', 'Directo'),
        ('booking', 'Booking.com'),
        ('airbnb', 'Airbnb'),
    ]

    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='reservas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='sitio')
    canal_reservacion = models.CharField(max_length=20, choices=CANALES_RESERVACION, default='sitio')

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
