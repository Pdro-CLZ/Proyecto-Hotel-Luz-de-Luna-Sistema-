from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from decimal import Decimal
from io import BytesIO
import calendar
import datetime
from django.db.models import Sum
from xhtml2pdf import pisa
from openpyxl import Workbook
from contabilidad.models import Contabilidad
from administracion.decorators import rol_requerido

#  FUNCIONES AUXILIARES
def meses():
    return [
        (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
        (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
        (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre")
    ]


def exportar_excel(datos, titulo):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Financiero"

    ws.append([titulo])
    ws.append([])
    ws.append(["Categoría", "Monto"])

    for fila in datos:
        ws.append([fila["categoria"], float(fila["total"])])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{titulo}.xlsx"'
    wb.save(response)
    return response


def exportar_pdf(template_name, context, nombre_archivo):
    template = get_template(template_name)
    html = template.render(context)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}.pdf"'
    return response



#  VISTA PRINCIPAL
@rol_requerido("Administrador","Empleado_Nivel1")
def reporte_financiero(request):
    hoy = datetime.date.today()
    mes = int(request.GET.get("mes", hoy.month))
    anio = int(request.GET.get("anio", hoy.year))
    tipo_reporte = request.GET.get("tipo", "mensual")

    # Determinar rango según tipo
    if tipo_reporte == "semanal":
        inicio = hoy - datetime.timedelta(days=hoy.weekday())
        fin = inicio + datetime.timedelta(days=6)
        titulo = "Balance Semanal"
    elif tipo_reporte == "anual":
        inicio = datetime.date(anio, 1, 1)
        fin = datetime.date(anio, 12, 31)
        titulo = "Balance Anual"
    else:
        inicio = datetime.date(anio, mes, 1)
        fin = datetime.date(anio, mes, calendar.monthrange(anio, mes)[1])
        titulo = "Balance Mensual"

    # Ingresos y egresos del periodo seleccionado
    ingresos = (
        Contabilidad.objects.filter(tipo="Ingreso", fecha__range=[inicio, fin])
        .values("categoria")
        .annotate(total=Sum("monto"))
        .order_by("categoria")
    )
    egresos = (
        Contabilidad.objects.filter(tipo="Gasto", fecha__range=[inicio, fin])
        .values("categoria")
        .annotate(total=Sum("monto"))
        .order_by("categoria")
    )
    total_ingresos = ingresos.aggregate(suma=Sum("total"))["suma"] or Decimal(0)
    total_egresos = egresos.aggregate(suma=Sum("total"))["suma"] or Decimal(0)
    utilidad = total_ingresos - total_egresos

    #  Mes anterior
    mes_anterior = mes - 1 if mes > 1 else 12
    anio_anterior = anio if mes > 1 else anio - 1
    inicio_mes_ant = datetime.date(anio_anterior, mes_anterior, 1)
    fin_mes_ant = datetime.date(anio_anterior, mes_anterior, calendar.monthrange(anio_anterior, mes_anterior)[1])

    ingresos_mes_ant = (
        Contabilidad.objects.filter(tipo="Ingreso", fecha__range=[inicio_mes_ant, fin_mes_ant])
        .aggregate(total=Sum("monto"))["total"] or Decimal(0)
    )
    egresos_mes_ant = (
        Contabilidad.objects.filter(tipo="Gasto", fecha__range=[inicio_mes_ant, fin_mes_ant])
        .aggregate(total=Sum("monto"))["total"] or Decimal(0)
    )
    utilidad_mes_ant = ingresos_mes_ant - egresos_mes_ant

    #  Año anterior completo
    inicio_anio_ant = datetime.date(anio - 1, 1, 1)
    fin_anio_ant = datetime.date(anio - 1, 12, 31)
    ingresos_anio_ant = (
        Contabilidad.objects.filter(tipo="Ingreso", fecha__range=[inicio_anio_ant, fin_anio_ant])
        .aggregate(total=Sum("monto"))["total"] or Decimal(0)
    )
    egresos_anio_ant = (
        Contabilidad.objects.filter(tipo="Gasto", fecha__range=[inicio_anio_ant, fin_anio_ant])
        .aggregate(total=Sum("monto"))["total"] or Decimal(0)
    )
    utilidad_anio_ant = ingresos_anio_ant - egresos_anio_ant

    #  Año actual completo
    inicio_anio_act = datetime.date(anio, 1, 1)
    fin_anio_act = datetime.date(anio, 12, 31)
    ingresos_anio_act = (
        Contabilidad.objects.filter(tipo="Ingreso", fecha__range=[inicio_anio_act, fin_anio_act])
        .aggregate(total=Sum("monto"))["total"] or Decimal(0)
    )
    egresos_anio_act = (
        Contabilidad.objects.filter(tipo="Gasto", fecha__range=[inicio_anio_act, fin_anio_act])
        .aggregate(total=Sum("monto"))["total"] or Decimal(0)
    )
    utilidad_anio_act = ingresos_anio_act - egresos_anio_act

    #  Exportar
    exportar = request.GET.get("exportar")
    if exportar == "excel":
        return exportar_excel(ingresos, f"Reporte_Financiero_{mes}_{anio}")
    elif exportar == "pdf":
        context_pdf = {
            "anio": anio,
            "mes": dict(meses())[mes],
            "ingresos": ingresos,
            "egresos": egresos,
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "utilidad": utilidad,
            "titulo": titulo,
        }
        return exportar_pdf("reporteria/reporte_financiero_pdf.html", context_pdf, f"Reporte_Financiero_{mes}_{anio}")

    #  Contexto para template
    context = {
        "meses": meses(),
        "mes": mes,
        "anio": anio,
        "tipo_reporte": tipo_reporte,
        "titulo": titulo,
        "ingresos": ingresos,
        "egresos": egresos,
        "total_ingresos": total_ingresos,
        "total_egresos": total_egresos,
        "utilidad": utilidad,
        # Comparaciones
        "ingresos_mes_ant": ingresos_mes_ant,
        "egresos_mes_ant": egresos_mes_ant,
        "utilidad_mes_ant": utilidad_mes_ant,
        "ingresos_anio_act": ingresos_anio_act,
        "egresos_anio_act": egresos_anio_act,
        "utilidad_anio_act": utilidad_anio_act,
        "ingresos_anio_ant": ingresos_anio_ant,
        "egresos_anio_ant": egresos_anio_ant,
        "utilidad_anio_ant": utilidad_anio_ant,
    }

    return render(request, "reporteria/reporte_financiero.html", context)

