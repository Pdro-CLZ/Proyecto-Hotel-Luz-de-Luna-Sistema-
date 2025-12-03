from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from reservas.models import Reserva, FechaReservada
import datetime

import openpyxl
from openpyxl.utils import get_column_letter

from reportlab.pdfgen import canvas
from io import BytesIO
from administracion.decorators import rol_requerido

ESTADOS_HABITACION = [
    ('ocupada', 'Ocupada'),
    ('disponible', 'Disponible'),
]

@rol_requerido("Administrador","Empleado_Nivel1")
def reporte_reservas(request):

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    estado_habitacion = request.GET.get('estado_habitacion')  
    canal_reservacion = request.GET.get('canal_reservacion') 
    exportar = request.GET.get('exportar')  

    reservas = Reserva.objects.select_related('habitacion', 'cliente').all()

    fi = ff = None

    if fecha_inicio and fecha_fin:
        try:
            fi = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            ff = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()

            if fi <= ff:
                #Reservas que empiezan o terminan dentro del rango
                reservas = reservas.filter(
                    fecha_inicio__gte=fi,
                    fecha_fin__lte=ff
                )
            
        except ValueError:
      
            pass


    if canal_reservacion:
        reservas = reservas.filter(canal_reservacion=canal_reservacion)


    total_reservas = reservas.count()
    total_monto = reservas.aggregate(total=Sum('total'))['total'] or 0

    # Exportar
    if exportar == 'excel':
        return exportar_reservas_excel(reservas)

    if exportar == 'pdf':
        return exportar_reservas_pdf(reservas)

    context = {
        'reservas': reservas,
        'total_reservas': total_reservas,
        'total_monto': total_monto,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'estado_habitacion': estado_habitacion,
        'canal_reservacion': canal_reservacion,
        'opciones_estado': ESTADOS_HABITACION,
        'opciones_canal': Reserva.CANALES_RESERVACION,
    }
    return render(request, 'reporteria/reporte_reservas.html', context)


def exportar_reservas_excel(reservas_qs):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reservas"

    columnas = [
        'ID', 'Cliente', 'Habitación', 'Fecha inicio',
        'Fecha fin', 'Total', 'Canal', 'Método de pago'
    ]
    ws.append(columnas)

    for r in reservas_qs:
        ws.append([
            r.id,
            str(r.cliente),
            r.habitacion.nombre,
            r.fecha_inicio.strftime('%Y-%m-%d'),
            r.fecha_fin.strftime('%Y-%m-%d'),
            float(r.total),
            r.get_canal_reservacion_display(),
            r.get_metodo_pago_display(),
        ])

    for col_num, _ in enumerate(columnas, 1):
        col_letter = get_column_letter(col_num)
        ws.column_dimensions[col_letter].width = 18

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=reporte_reservas.xlsx'
    wb.save(response)
    return response


def exportar_reservas_pdf(reservas_qs):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    x = 50
    y = 800
    p.drawString(x, y, "Reporte de Reservas")
    y -= 30

    for r in reservas_qs:
        linea = f"ID {r.id} - {r.cliente} - {r.habitacion.nombre} - {r.fecha_inicio} a {r.fecha_fin} - {r.total}"
        p.drawString(x, y, linea)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=\"reporte_reservas.pdf\"'
    response.write(pdf)
    return response
