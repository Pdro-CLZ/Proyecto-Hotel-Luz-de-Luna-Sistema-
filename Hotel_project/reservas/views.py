from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date, datetime
from django.db import transaction
from django.contrib import messages
from .models import Habitacion, FechaReservada, Cliente, Reserva, PrecioHabitacion
from decimal import Decimal


@login_required
def index_reservas(request):
    hoy = timezone.localdate()

    inicio_semana = hoy - timedelta(days=hoy.weekday())
    dias = [inicio_semana + timedelta(days=i) for i in range(7)]
    fin_semana = dias[-1]

    habitaciones = Habitacion.objects.all().order_by('id')

    fechas_reservadas = FechaReservada.objects.filter(
        fecha__range=(inicio_semana, fin_semana)
    ).select_related('habitacion', 'reserva__cliente')

    reservado_map = {}
    for fr in fechas_reservadas:
        reservado_map[(fr.habitacion_id, fr.fecha)] = fr

    grid = []
    for hab in habitaciones:
        fila = {'habitacion': hab, 'celdas': []}
        for dia in dias:
            fila['celdas'].append(reservado_map.get((hab.id, dia)))
        grid.append(fila)

    context = {
        'habitaciones': habitaciones,
        'dias': dias,
        'grid': grid,
        'inicio_semana': inicio_semana,
        'fin_semana': fin_semana,
    }
    return render(request, 'index_reservas.html', context)


@login_required
def agregar_reserva(request):
    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return render(request, "agregar_reserva.html", {
                "error": "Por favor selecciona ambas fechas."
            })

        fecha_inicio = date.fromisoformat(fecha_inicio)
        fecha_fin = date.fromisoformat(fecha_fin)

        if fecha_fin < fecha_inicio:
            return render(request, "agregar_reserva.html", {
                "error": "La fecha de fin no puede ser anterior a la de inicio."
            })

        reservadas = FechaReservada.objects.filter(
            fecha__range=(fecha_inicio, fecha_fin)
        ).values_list("habitacion_id", flat=True)

        disponibles = Habitacion.objects.exclude(id__in=reservadas).order_by("id")

        resultados = []
        for hab in disponibles:
            amenidades = hab.amenidades.all()
            precios = PrecioHabitacion.objects.filter(
                habitacion=hab, fecha__range=(fecha_inicio, fecha_fin)
            )

            noches = (fecha_fin - fecha_inicio).days + 1
            precio_total = sum(p.precio for p in precios) if precios else 0

            resultados.append({
                "habitacion": hab,
                "amenidades": amenidades,
                "precio_total": precio_total,
                "noches": noches,
            })

        return render(request, "habitaciones_disponibles.html", {
            "disponibles": resultados,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
        })

    return render(request, "agregar_reserva.html")


@login_required
def buscar_cliente(request):
    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        habitacion_id = request.POST.get('habitacion_id')

        cliente = Cliente.objects.filter(identificacion=identificacion).first()
        if cliente:
            return redirect('nueva_reserva_cliente',
                            habitacion_id=habitacion_id,
                            fecha_inicio=fecha_inicio,
                            fecha_fin=fecha_fin,
                            cliente_id=cliente.id)
        else:
            messages.info(request, 'Cliente no encontrado, por favor complete los datos.')
            return redirect('nueva_reserva_cliente',
                            habitacion_id=habitacion_id,
                            fecha_inicio=fecha_inicio,
                            fecha_fin=fecha_fin)

    return HttpResponse("Método no permitido.", status=405)


@login_required
def nueva_reserva_cliente(request, habitacion_id, fecha_inicio, fecha_fin, cliente_id=None):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    cliente = Cliente.objects.filter(id=cliente_id).first()

    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    if request.method == 'POST':
        if not cliente:
            cliente = Cliente.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                telefono=request.POST['telefono'],
                correo=request.POST['correo'],
                identificacion=request.POST['identificacion']
            )

        metodo_pago = request.POST.get('metodo_pago')
        canal_reservacion = request.POST.get('canal_reservacion')

        return redirect('confirmar_reserva',
                        habitacion_id=habitacion.id,
                        fecha_inicio=fecha_inicio.strftime("%Y-%m-%d"),
                        fecha_fin=fecha_fin.strftime("%Y-%m-%d"),
                        cliente_id=cliente.id,
                        metodo_pago=metodo_pago,
                        canal_reservacion=canal_reservacion)

    return render(request, 'nueva_reserva_cliente.html', {
        'habitacion': habitacion,
        'cliente': cliente,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


@login_required
@transaction.atomic
def confirmar_reserva(request, habitacion_id, fecha_inicio, fecha_fin, cliente_id, metodo_pago, canal_reservacion):
    """Resumen final de la reserva y confirmación"""
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    precios = PrecioHabitacion.objects.filter(
        habitacion=habitacion,
        fecha__range=(fecha_inicio, fecha_fin)
    )
    total = sum([p.precio for p in precios]) or Decimal('0.00')

    if request.method == 'POST':
        reserva = Reserva.objects.create(
            habitacion=habitacion,
            cliente=cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            total=total,
            metodo_pago=metodo_pago,
            canal_reservacion=canal_reservacion,
        )
        dias_reserva = (fecha_fin - fecha_inicio).days + 1
        for i in range(dias_reserva):
            f = fecha_inicio + timedelta(days=i)
            FechaReservada.objects.create(habitacion=habitacion, fecha=f, reserva=reserva)

        messages.success(request, 'Reserva creada exitosamente.')
        return redirect('index_reservas')

    return render(request, 'confirmar_reserva.html', {
        'habitacion': habitacion,
        'cliente': cliente,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total': total,
        'metodo_pago': metodo_pago,
        'canal_reservacion': canal_reservacion,
    })

from datetime import date, timedelta
from calendar import monthrange
from django.utils.timezone import now
from .models import Habitacion, PrecioHabitacion
from django.shortcuts import render, redirect
from django.contrib import messages

def precios_calendario(request):
    hoy = now().date()
    año = int(request.GET.get("year", hoy.year))
    mes = int(request.GET.get("month", hoy.month))

    # Calcular mes anterior y siguiente
    if mes == 1:
        prev_month = 12
        prev_year = año - 1
    else:
        prev_month = mes - 1
        prev_year = año

    if mes == 12:
        next_month = 1
        next_year = año + 1
    else:
        next_month = mes + 1
        next_year = año

    dias_mes = monthrange(año, mes)[1]
    dias = list(range(1, dias_mes + 1))

    rango_fechas = [
        date(año, mes, d).isoformat()
        for d in dias
    ]

    habitaciones = Habitacion.objects.all()

    precios_map = {}
    for hab in habitaciones:
        precios_map[hab.id] = {}
        precios = PrecioHabitacion.objects.filter(
            habitacion=hab,
            fecha__year=año,
            fecha__month=mes
        )
        for p in precios:
            precios_map[hab.id][p.fecha.isoformat()] = p.precio

    mes_nombre = date(año, mes, 1).strftime("%B")

    return render(request, "reservas/precios_calendario.html", {
        "habitaciones": habitaciones,
        "dias": dias,
        "rango_fechas": rango_fechas,
        "precios_map": precios_map,
        "mes_nombre": mes_nombre,
        "año": año,

        # navegación
        "prev_month": prev_month,
        "prev_year": prev_year,
        "next_month": next_month,
        "next_year": next_year,
    })


def asignar_precio_rango(request):
    if request.method == "POST":
        hab_id = request.POST.get("habitacion_id")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        precio = request.POST.get("precio")

        if not (hab_id and fecha_inicio and fecha_fin):
            messages.error(request, "Datos incompletos.")
            return redirect("precios_calendario")

        fecha1 = date.fromisoformat(fecha_inicio)
        fecha2 = date.fromisoformat(fecha_fin)

        actual = fecha1
        while actual <= fecha2:
            PrecioHabitacion.objects.update_or_create(
                habitacion_id=hab_id,
                fecha=actual,
                defaults={"precio": precio}
            )
            actual += timedelta(days=1)

        messages.success(request, "Precios actualizados.")
        return redirect("precios_calendario")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import timedelta
from .models import PrecioHabitacion, Habitacion
from .forms import PrecioRangoForm


def gestionar_precios(request):
    precios = PrecioHabitacion.objects.select_related("habitacion").order_by("-fecha")
    return render(request, "reservas/gestionar_precios.html", {"precios": precios})


def agregar_precio_rango(request):
    if request.method == "POST":
        form = PrecioRangoForm(request.POST)
        if form.is_valid():
            habitacion = form.cleaned_data["habitacion"]
            fecha_inicio = form.cleaned_data["fecha_inicio"]
            fecha_fin = form.cleaned_data["fecha_fin"]
            precio = form.cleaned_data["precio"]

            if fecha_fin < fecha_inicio:
                messages.error(request, "La fecha final no puede ser menor a la inicial.")
                return redirect("agregar_precio_rango")

            # Crear o actualizar precios por día
            fecha = fecha_inicio
            dias_creados = 0
            while fecha <= fecha_fin:
                obj, creado = PrecioHabitacion.objects.update_or_create(
                    habitacion=habitacion,
                    fecha=fecha,
                    defaults={"precio": precio}
                )
                if creado:
                    dias_creados += 1
                fecha += timedelta(days=1)

            messages.success(request, f"Precios registrados para {dias_creados} días.")
            return redirect("gestionar_precios")
    else:
        form = PrecioRangoForm()

    return render(request, "reservas/agregar_precio_rango.html", {"form": form})


def eliminar_precio(request, id):
    precio = get_object_or_404(PrecioHabitacion, id=id)
    precio.delete()
    messages.success(request, "Precio eliminado correctamente.")
    return redirect("gestionar_precios")
