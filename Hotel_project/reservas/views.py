from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date, datetime
from django.db import transaction
from django.contrib import messages
from sitio_web.models import Cliente  
from administracion.models import Usuario 
from .models import Habitacion, FechaReservada, Reserva, PrecioHabitacion
from decimal import Decimal
from django.contrib.auth.hashers import make_password

@login_required
def index_reservas(request):
    fecha_seleccionada = request.GET.get("fecha")

    if fecha_seleccionada:
        try:
            fecha_base = date.fromisoformat(fecha_seleccionada)
        except:
            fecha_base = timezone.localdate()
    else:
        fecha_base = timezone.localdate()

    inicio_semana = fecha_base - timedelta(days=fecha_base.weekday())
    dias = [inicio_semana + timedelta(days=i) for i in range(7)]
    fin_semana = dias[-1]
    habitaciones = Habitacion.objects.all().order_by('id')

    fechas_reservadas = FechaReservada.objects.filter(
        fecha__range=(inicio_semana, fin_semana)
    ).select_related('habitacion', 'reserva__cliente__usuario')

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

        cliente = Cliente.objects.select_related('usuario').filter(
            usuario__cedula=identificacion
        ).first()

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
    cliente = Cliente.objects.filter(id=cliente_id).select_related("usuario").first()

    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    if request.method == 'POST':
        if not cliente:

            usuario = Usuario.objects.create(
                username=request.POST['identificacion'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                cedula=request.POST['identificacion'],
                email=request.POST['correo'],
                password=make_password('Pass123!'),
                rol_id=3,
            )
            
            cliente = Cliente.objects.create(
                usuario=usuario,
                telefono=request.POST['telefono'],
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
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    cliente = get_object_or_404(Cliente.objects.select_related("usuario"), pk=cliente_id)

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
