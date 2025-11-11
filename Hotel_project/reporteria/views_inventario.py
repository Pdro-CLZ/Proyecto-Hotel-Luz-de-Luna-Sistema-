from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from openpyxl import Workbook
from inventario.models import Inventario
from datetime import timedelta


# Exportar Excel
def exportar_excel(datos, titulo):
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventario"
    ws.append([titulo])
    ws.append([])
    ws.append(["Producto", "Descripción", "Tipo", "Cantidad", "Estado"])

    for fila in datos:
        ws.append(fila)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{titulo}.xlsx"'
    wb.save(response)
    return response


#  Exportar PDF
def exportar_pdf(template_name, context, nombre_archivo):
    template = get_template(template_name)
    html = template.render(context)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}.pdf"'
    return response


#  Vista principal
def reporte_inventario(request):
    tipo_filtro = request.GET.get("tipo", "")
    bajo_stock = request.GET.get("bajo_stock", "")
    producto_id = request.GET.get("producto")

    productos = Inventario.objects.all().order_by("nombre")
    if tipo_filtro:
        productos = productos.filter(tipo__iexact=tipo_filtro)


    if bajo_stock:
        productos = productos.filter(cantidad__lt=10)

    exportar = request.GET.get("exportar")
    if exportar == "excel":
        filas = []
        for p in productos:
            estado = "Bajo stock" if p.cantidad < 10 else "Normal"
            filas.append([p.nombre, p.descripcion, p.tipo, p.cantidad, estado])
        return exportar_excel(filas, "Reporte_Inventario")

    elif exportar == "pdf":
        context_pdf = {
            "productos": productos,
            "tipo_filtro": tipo_filtro,
            "bajo_stock": bajo_stock,
        }
        return exportar_pdf("reporteria/reporte_inventario_pdf.html", context_pdf, "Reporte_Inventario")

    context = {
        "productos": productos,
        "tipo_filtro": tipo_filtro,
        "bajo_stock": bajo_stock,
    }
    return render(request, "reporteria/reporte_inventario.html", context)
