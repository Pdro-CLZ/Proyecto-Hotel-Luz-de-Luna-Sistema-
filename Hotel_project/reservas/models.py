from django.db import models

class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    identificacion = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    desayuno_incluido = models.BooleanField(default=False)

    def __str__(self):
        return f"Habitación {self.numero}"


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    canal_reserva = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente}"
