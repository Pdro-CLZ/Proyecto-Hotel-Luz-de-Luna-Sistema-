from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Avg
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from openpyxl import Workbook
from datetime import date
from personal.models import Empleado, Asistencia
from administracion.models import Rol
from administracion.decorators import rol_requerido

#  Exportar a Excel
def exportar_excel(datos, titulo):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rendimiento Personal"
    ws.append([titulo])
    ws.append([])
    ws.append(["Empleado", "Área", "Asistencias", "Promedio Horas", "Puntualidad", "Tareas Completadas"])

    for fila in datos:
        ws.append(fila)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{titulo}.xlsx"'
    wb.save(response)
    return response


#  Exportar a PDF
def exportar_pdf(template_name, context, nombre_archivo):
    template = get_template(template_name)
    html = template.render(context)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}.pdf"'
    return response


#  Vista principal del reporte
@rol_requerido("Administrador","Empleado_Nivel1")
def reporte_personal(request):
    mes = int(request.GET.get("mes", date.today().month))
    anio = int(request.GET.get("anio", date.today().year))
    area_id = request.GET.get("area")
    empleado_id = request.GET.get("empleado")

    #  Obtener roles (áreas de trabajo)
    areas = Rol.objects.all().order_by("nombre")

    #  Filtrar asistencias del mes/año
    asistencias = Asistencia.objects.filter(fecha__year=anio, fecha__month=mes)

    empleados = Empleado.objects.select_related("usuario").all()
    if area_id:
        empleados = empleados.filter(usuario__rol_id=area_id)

    data = []
    for emp in empleados:
        asist_emp = asistencias.filter(empleado=emp)
        total_asistencias = asist_emp.count()
        promedio_horas = asist_emp.aggregate(prom=Avg("horas_trabajadas"))["prom"] or 0

        # Puntualidad = % de llegadas antes de las 8:00
        puntuales = asist_emp.filter(hora_llegada__lte="08:00:00").count()
        puntualidad_pct = round((puntuales / total_asistencias) * 100, 1) if total_asistencias > 0 else 0

        # Tareas completadas (solo si existe TareaLimpieza)
        try:
            from limpieza.models import TareaLimpieza
            tareas_completadas = TareaLimpieza.objects.filter(usuario_modifica=emp.usuario, estado="Realizada").count()
        except Exception:
            tareas_completadas = 0

        data.append({
            "empleado": emp,
            "area": emp.usuario.rol.nombre if hasattr(emp.usuario, "rol") else "Sin área",
            "total_asistencias": total_asistencias,
            "promedio_horas": round(promedio_horas, 2),
            "puntualidad_pct": puntualidad_pct,
            "tareas_completadas": tareas_completadas,
        })

    #  Detalle del empleado seleccionado (para gráfico y tabla)
    detalle_asistencias = None
    grafico_dias = []
    grafico_valores = []
    if empleado_id:
        detalle_asistencias = asistencias.filter(empleado_id=empleado_id).order_by("fecha")
        grafico_dias = [a.fecha.strftime("%d") for a in detalle_asistencias]
        grafico_valores = [float(a.horas_trabajadas or 0) for a in detalle_asistencias]

    #  Exportar a Excel o PDF
    exportar = request.GET.get("exportar")
    if exportar == "excel":
        filas = []
        for d in data:
            filas.append([
                f"{d['empleado'].nombre} {d['empleado'].apellido}",
                d["area"],
                d["total_asistencias"],
                d["promedio_horas"],
                f"{d['puntualidad_pct']}%",
                d["tareas_completadas"],
            ])
        return exportar_excel(filas, f"Rendimiento_Personal_{mes}_{anio}")

    elif exportar == "pdf":
        context_pdf = {
            "data": data,
            "mes": mes,
            "anio": anio,
            "area": next((a.nombre for a in areas if str(a.id) == str(area_id)), "Todas"),
        }
        return exportar_pdf("reporteria/reporte_personal_pdf.html", context_pdf, f"Rendimiento_Personal_{mes}_{anio}")

    #  Render normal
    context = {
        "areas": areas,
        "data": data,
        "area_id": area_id,
        "empleado_id": empleado_id,
        "mes": mes,
        "anio": anio,
        "detalle_asistencias": detalle_asistencias,
        "grafico_dias": grafico_dias,
        "grafico_valores": grafico_valores,
    }
    return render(request, "reporteria/reporte_personal.html", context)
