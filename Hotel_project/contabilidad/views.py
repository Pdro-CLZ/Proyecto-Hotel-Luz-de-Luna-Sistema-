from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.contrib import messages
from django.utils import timezone
from .models import Contabilidad, CierreMensual, CierreAnual
import datetime
from administracion.decorators import rol_requerido
from .models import CierreMensual, CierreAnual

# PANEL PRINCIPAL
@rol_requerido("Administrador", "Empleado_Nivel1")
def contabilidad_panel(request):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')

    hoy = datetime.date.today()
    mes = int(mes) if mes else hoy.month
    anio = int(anio) if anio else hoy.year

    # Validación de selección de fecha inválida
    if anio > hoy.year or (anio == hoy.year and mes > hoy.month):
        messages.error(request, "Fecha no disponible.")
        contexto = {
            'mes': hoy.month,
            'anio': hoy.year,
            'total_ingresos': 0,
            'total_gastos': 0,
            'utilidad': 0,
            'sin_datos': True,
            'ingresos': [],
            'gastos': []
        }
        return render(request, 'contabilidad/index.html', contexto)

    # Filtrar registros válidos
    ingresos_qs = Contabilidad.objects.filter(
        Q(tipo__iexact='Ingreso'),
        fecha__month=mes, fecha__year=anio
    )
    gastos_qs = Contabilidad.objects.filter(
        Q(tipo__iexact='Gasto'),
        fecha__month=mes, fecha__year=anio
    )

    # Calcular totales
    total_ingresos = ingresos_qs.aggregate(total=Sum('monto'))['total'] or 0
    total_gastos = gastos_qs.aggregate(total=Sum('monto'))['total'] or 0
    utilidad = total_ingresos - total_gastos
    sin_datos = not ingresos_qs.exists() and not gastos_qs.exists()

    contexto = {
        'mes': mes,
        'anio': anio,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'utilidad': utilidad,
        'sin_datos': sin_datos,
        'ingresos': ingresos_qs,
        'gastos': gastos_qs,
    }
    return render(request, 'contabilidad/index.html', contexto)


# AGREGAR INGRESO
@rol_requerido("Administrador", "Empleado_Nivel1")
def agregar_ingreso(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        metodo_pago = request.POST.get('metodo_pago')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        monto = request.POST.get('monto')

        if not (fecha and metodo_pago and categoria and descripcion and monto):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('agregar_ingreso')

        fecha_dt = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()

        # Verificar si el mes o año ya tienen cierre
        if CierreMensual.objects.filter(mes=fecha_dt.month, anio=fecha_dt.year).exists():
            messages.error(request, f"No se puede registrar un ingreso: el mes {fecha_dt.month}/{fecha_dt.year} ya está cerrado.")
            return redirect('contabilidad_panel')

        if CierreAnual.objects.filter(anio=fecha_dt.year).exists():
            messages.error(request, f"No se puede registrar un ingreso: el año {fecha_dt.year} ya está cerrado.")
            return redirect('contabilidad_panel')

        try:
            monto = float(monto)
            if monto <= 0:
                messages.error(request, "El monto debe ser mayor a 0.")
                return redirect('agregar_ingreso')
        except ValueError:
            messages.error(request, "Solo se permiten números en el campo monto.")
            return redirect('agregar_ingreso')

        Contabilidad.objects.create(
            fecha=fecha,
            tipo='Ingreso',
            metodo_pago=metodo_pago,
            categoria=categoria,
            descripcion=descripcion,
            monto=monto
        )
        messages.success(request, "Ingreso registrado correctamente.")
        return redirect('contabilidad_panel')

    return render(request, 'contabilidad/agregar_ingreso.html')


# AGREGAR GASTO
@rol_requerido("Administrador", "Empleado_Nivel1")
def agregar_gasto(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        metodo_pago = request.POST.get('metodo_pago')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        monto = request.POST.get('monto')

        if not (fecha and metodo_pago and categoria and descripcion and monto):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('agregar_gasto')

        fecha_dt = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()

        # Verificar si el mes o año ya tienen cierre
        if CierreMensual.objects.filter(mes=fecha_dt.month, anio=fecha_dt.year).exists():
            messages.error(request, f"No se puede registrar un gasto: el mes {fecha_dt.month}/{fecha_dt.year} ya está cerrado.")
            return redirect('contabilidad_panel')

        if CierreAnual.objects.filter(anio=fecha_dt.year).exists():
            messages.error(request, f"No se puede registrar un gasto: el año {fecha_dt.year} ya está cerrado.")
            return redirect('contabilidad_panel')

        try:
            monto = float(monto)
            if monto <= 0:
                messages.error(request, "El monto debe ser mayor a 0.")
                return redirect('agregar_gasto')
        except ValueError:
            messages.error(request, "Solo se permiten números en el campo monto.")
            return redirect('agregar_gasto')

        Contabilidad.objects.create(
            fecha=fecha,
            tipo='Gasto',
            metodo_pago=metodo_pago,
            categoria=categoria,
            descripcion=descripcion,
            monto=monto
        )
        messages.success(request, "Gasto registrado correctamente.")
        return redirect('contabilidad_panel')

    return render(request, 'contabilidad/agregar_gasto.html')



# EDITAR INGRESO
@rol_requerido("Administrador", "Empleado_Nivel1")
def editar_ingreso(request, id):
    ingreso = get_object_or_404(Contabilidad, id=id, tipo='Ingreso')

    if request.method == 'POST':
        ingreso.fecha = request.POST.get('fecha')
        ingreso.metodo_pago = request.POST.get('metodo_pago')
        ingreso.categoria = request.POST.get('categoria')
        ingreso.descripcion = request.POST.get('descripcion')
        ingreso.monto = request.POST.get('monto')

        try:
            ingreso.monto = float(ingreso.monto)
            if ingreso.monto <= 0:
                messages.error(request, "El monto debe ser mayor a 0.")
                return redirect('editar_ingreso', id=id)
        except ValueError:
            messages.error(request, "Solo se permiten números.")
            return redirect('editar_ingreso', id=id)

        ingreso.save()
        messages.success(request, "Ingreso actualizado correctamente.")
        return redirect('contabilidad_panel')

    return render(request, 'contabilidad/editar_ingreso.html', {'registro': ingreso})


# EDITAR GASTO
@rol_requerido("Administrador", "Empleado_Nivel1")
def editar_gasto(request, id):
    gasto = get_object_or_404(Contabilidad, id=id, tipo='Gasto')

    if request.method == 'POST':
        gasto.fecha = request.POST.get('fecha')
        gasto.metodo_pago = request.POST.get('metodo_pago')
        gasto.categoria = request.POST.get('categoria')
        gasto.descripcion = request.POST.get('descripcion')
        gasto.monto = request.POST.get('monto')

        try:
            gasto.monto = float(gasto.monto)
            if gasto.monto <= 0:
                messages.error(request, "El monto debe ser mayor a 0.")
                return redirect('editar_gasto', id=id)
        except ValueError:
            messages.error(request, "Solo se permiten números.")
            return redirect('editar_gasto', id=id)

        gasto.save()
        messages.success(request, "Gasto actualizado correctamente.")
        return redirect('contabilidad_panel')

    return render(request, 'contabilidad/editar_gasto.html', {'registro': gasto})

# ====== CIERRE MENSUAL ======
@rol_requerido("Administrador", "Empleado_Nivel1")
def cierre_mensual(request):
    hoy = datetime.date.today()

    if request.method == 'POST':
        mes = int(request.POST.get('mes'))
        anio = int(request.POST.get('anio'))

        # Validar fecha futura
        if anio > hoy.year or (anio == hoy.year and mes > hoy.month):
            messages.error(request, "Fecha no disponible.")
            return render(request, 'contabilidad/cierre_mensual.html', {'anio': anio})

        #  Validar si el mes aún no ha finalizado
        if anio == hoy.year and mes == hoy.month:
            messages.error(request, "Cierre no disponible: el mes aún no ha finalizado.")
            return render(request, 'contabilidad/cierre_mensual.html', {'anio': anio})

        # Validar si el cierre ya existe
        if CierreMensual.objects.filter(mes=mes, anio=anio).exists():
            messages.error(request, f"Ya existe un cierre mensual para {mes}/{anio}.")
            return render(request, 'contabilidad/cierre_mensual.html', {'anio': anio})

        # Calcular totales
        ingresos = Contabilidad.objects.filter(
            tipo='Ingreso', fecha__month=mes, fecha__year=anio
        ).aggregate(total=Sum('monto'))['total'] or 0

        gastos = Contabilidad.objects.filter(
            tipo='Gasto', fecha__month=mes, fecha__year=anio
        ).aggregate(total=Sum('monto'))['total'] or 0

        utilidad = ingresos - gastos

        # Guardar cierre
        CierreMensual.objects.create(
            mes=mes,
            anio=anio,
            total_ingresos=ingresos,
            total_gastos=gastos,
            utilidad=utilidad
        )

        messages.success(request, f"Cierre mensual del {mes}/{anio} generado correctamente.")
        return render(request, 'contabilidad/cierre_mensual.html', {
            'mes': mes,
            'anio': anio,
            'ingresos': ingresos,
            'gastos': gastos,
            'utilidad': utilidad
        })

    return render(request, 'contabilidad/cierre_mensual.html', {'anio': hoy.year})



# ====== CIERRE ANUAL ======
@rol_requerido("Administrador", "Empleado_Nivel1")
def cierre_anual(request):
    hoy = datetime.date.today()

    if request.method == 'POST':
        anio = int(request.POST.get('anio'))

        # Validar si el año es futuro
        if anio > hoy.year:
            messages.error(request, "Fecha no disponible para visualizar datos.")
            return render(request, 'contabilidad/cierre_anual.html', {'anio': anio})

        # Validar si el año actual aún no ha finalizado
        if anio == hoy.year:
            messages.error(request, " Cierre no disponible: el año aún no ha finalizado.")
            return render(request, 'contabilidad/cierre_anual.html', {'anio': anio})

        # Consultar todos los registros del año
        ingresos_lista = Contabilidad.objects.filter(tipo='Ingreso', fecha__year=anio)
        gastos_lista = Contabilidad.objects.filter(tipo='Gasto', fecha__year=anio)

        # Validar si el cierre anual ya existe
        cierre_existente = CierreAnual.objects.filter(anio=anio).first()
        if cierre_existente:
            messages.warning(request, f"El año {anio} ya fue cerrado anteriormente.")
            
            # Mostrar los datos guardados y el resumen
            return render(request, 'contabilidad/cierre_anual.html', {
                'anio': anio,
                'ingresos': cierre_existente.total_ingresos,
                'gastos': cierre_existente.total_gastos,
                'utilidad': cierre_existente.utilidad,
                'ingresos_lista': ingresos_lista,
                'gastos_lista': gastos_lista,
                'cerrado': True
            })

        # Calcular totales del año
        total_ingresos = ingresos_lista.aggregate(total=Sum('monto'))['total'] or 0
        total_gastos = gastos_lista.aggregate(total=Sum('monto'))['total'] or 0
        utilidad = total_ingresos - total_gastos

        # Guardar cierre anual
        CierreAnual.objects.create(
            anio=anio,
            total_ingresos=total_ingresos,
            total_gastos=total_gastos,
            utilidad=utilidad
        )

        messages.success(request, f"Cierre anual del {anio} generado correctamente.")
        return render(request, 'contabilidad/cierre_anual.html', {
            'anio': anio,
            'ingresos': total_ingresos,
            'gastos': total_gastos,
            'utilidad': utilidad,
            'ingresos_lista': ingresos_lista,
            'gastos_lista': gastos_lista,
            'cerrado': False
        })

    
    return render(request, 'contabilidad/cierre_anual.html', {'anio': hoy.year})

