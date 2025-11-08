from django.core.management.base import BaseCommand
from datetime import date, timedelta
from reservas.models import Amenidad, Habitacion, PrecioHabitacion, Reserva
from sitio_web.models import Cliente


class Command(BaseCommand):
    help = "Puebla la base de datos con habitaciones, precios, amenidades y una reserva de ejemplo."

    def handle(self, *args, **kwargs):
        # --- 1️⃣ Crear Amenidades ---
        amenidades_nombres = ["Hamaca", "Piscina", "Refrigeradora", "Parqueo", "Wifi"]
        amenidades = []
        for nombre in amenidades_nombres:
            a, _ = Amenidad.objects.get_or_create(nombre=nombre)
            amenidades.append(a)

        self.stdout.write(self.style.SUCCESS(f"{len(amenidades)} amenidades creadas o existentes."))

        # --- 2️⃣ Crear Habitaciones ---
        habitaciones_data = [
            {"numero": 1, "descripcion": "1 cama grande", "precio_base": 60, "precio_alta": 80, "cocina": False},
            {"numero": 2, "descripcion": "1 cama grande", "precio_base": 60, "precio_alta": 80, "cocina": False},
            {"numero": 3, "descripcion": "1 cama grande y 1 pequeña", "precio_base": 80, "precio_alta": 100, "cocina": False},
            {"numero": 4, "descripcion": "1 cama grande y 2 pequeñas con cocina", "precio_base": 100, "precio_alta": 120, "cocina": True},
            {"numero": 5, "descripcion": "1 cama grande y 2 pequeñas con cocina", "precio_base": 100, "precio_alta": 120, "cocina": True},
            {"numero": 6, "descripcion": "1 cama grande y 2 pequeñas con cocina", "precio_base": 100, "precio_alta": 120, "cocina": True},
            {"numero": 7, "descripcion": "1 cama grande con cocina", "precio_base": 120, "precio_alta": 140, "cocina": True},
            {"numero": 8, "descripcion": "1 cama grande con cocina", "precio_base": 120, "precio_alta": 140, "cocina": True},
        ]

        habitaciones = []
        for hdata in habitaciones_data:
            h, _ = Habitacion.objects.get_or_create(
                numero=hdata["numero"],
                defaults={
                    "descripcion": hdata["descripcion"],
                    "tiene_cocina": hdata["cocina"]
                }
            )
            h.amenidades.set(amenidades)
            habitaciones.append(h)

        self.stdout.write(self.style.SUCCESS(f"{len(habitaciones)} habitaciones creadas o existentes."))

        # --- 3️⃣ Crear Precios por Día ---
        start_date = date.today()
        end_date = date(2026, 12, 31)
        current_date = start_date
        count = 0

        while current_date <= end_date:
            mes = current_date.month
            temporada_alta = mes in [12, 1, 2, 3, 4, 5]
            for hdata, habitacion in zip(habitaciones_data, habitaciones):
                precio = hdata["precio_alta"] if temporada_alta else hdata["precio_base"]
                PrecioHabitacion.objects.get_or_create(
                    habitacion=habitacion,
                    fecha=current_date,
                    defaults={"precio": precio}
                )
                count += 1
            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(f"{count} precios creados o existentes para todas las habitaciones."))

        # --- 4️⃣ Crear Cliente ---
        cliente, _ = Cliente.objects.get_or_create(
            identificacion="123456789",
            defaults={
                "nombre": "Juan",
                "apellido": "Pérez",
                "telefono": "88888888",
                "correo": "juanperez@example.com"
            }
        )
        self.stdout.write(self.style.SUCCESS(f"Cliente creado o existente: {cliente}"))

        # --- 5️⃣ Crear una Reserva ---
        fecha_inicio = date(2025, 11, 9)
        fecha_fin = fecha_inicio + timedelta(days=1)
        habitacion = Habitacion.objects.get(numero=1)

        reserva, creada = Reserva.objects.get_or_create(
            habitacion=habitacion,
            cliente=cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            defaults={"numero_personas": 2}
        )

        if creada:
            self.stdout.write(self.style.SUCCESS("Reserva creada exitosamente."))
        else:
            self.stdout.write(self.style.WARNING("La reserva ya existía."))
