from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from openpyxl import Workbook
from datetime import datetime, timedelta
from administracion.decorators import rol_requerido
from limpieza.models import TareaLimpieza, ZonaLimpieza
from administracion.models import Usuario

# Función auxiliar para exportar Excel
def exportar_excel(datos, titulo):
    wb = Workbook()
    ws = wb.active
    ws.title = "Historial Limpieza"
    ws.append([titulo])
    ws.append([])
    ws.append(["Habitación", "Tarea", "Empleado", "Estado", "Fecha modificación"])

    for fila in datos:
        ws.append(fila)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{titulo}.xlsx"'
    wb.save(response)
    return response


# Función auxiliar para exportar PDF
def exportar_pdf(template_name, context, nombre_archivo):
    template = get_template(template_name)
    html = template.render(context)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}.pdf"'
    return response

@rol_requerido("Administrador","Empleado_Nivel1")
def reporte_limpieza(request):
    habitaciones = ZonaLimpieza.objects.filter(is_habitacion=True).order_by("nombre")
    tareas = TareaLimpieza.objects.select_related("zona", "usuario_modifica").order_by("-fecha_modificacion")

    #  LISTA DE ENCARGADOS 
    encargados = Usuario.objects.filter(tareas_modificadas__isnull=False).distinct().order_by("id")

    #  Filtros
    habitacion_id   = request.GET.get("habitacion")
    encargado_id    = request.GET.get("encargado") 
    fecha_inicio    = request.GET.get("desde")
    fecha_fin       = request.GET.get("hasta")
    mostrar_pendientes = request.GET.get("pendientes")

    if habitacion_id:
        tareas = tareas.filter(zona_id=habitacion_id)
    if encargado_id:
        tareas = tareas.filter(usuario_modifica_id=encargado_id)

  
    if fecha_inicio:
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            tareas = tareas.filter(fecha_modificacion__gte=fecha_inicio_obj)
        except ValueError:
            pass

    if fecha_fin:
        try:
            fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1)
            tareas = tareas.filter(fecha_modificacion__lt=fecha_fin_obj)
        except ValueError:
            pass

    if mostrar_pendientes:
        tareas = tareas.filter(estado="Pendiente")

    
    semana_actual = datetime.now().isocalendar().week
    frecuencia = (
        TareaLimpieza.objects.filter(fecha_modificacion__week=semana_actual, zona__is_habitacion=True)
        .values("zona__nombre")
        .annotate(total=Count("id"))
        .order_by("zona__nombre")
    )


    exportar = request.GET.get("exportar")
    if exportar == "excel":
        filas = []
        for t in tareas:
            filas.append([
                t.zona.nombre,
                t.nombre,
                t.usuario_modifica.username if t.usuario_modifica else "—",
                t.estado,
                t.fecha_modificacion.strftime("%Y-%m-%d %H:%M"),
            ])
        return exportar_excel(filas, "Historial_Limpieza")
    elif exportar == "pdf":
        context_pdf = {
            "tareas": tareas,
            "habitaciones": habitaciones,
            "frecuencia": frecuencia,
        }
        return exportar_pdf("reporteria/reporte_limpieza_pdf.html", context_pdf, "Historial_Limpieza")

    context = {
        "habitaciones": habitaciones,
        "encargados": encargados,           
        "tareas": tareas,
        "frecuencia": frecuencia,
        "habitacion_id": habitacion_id,
        "encargado_id": encargado_id,       
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "mostrar_pendientes": mostrar_pendientes,
    }
    return render(request, "reporteria/reporte_limpieza.html", context)


