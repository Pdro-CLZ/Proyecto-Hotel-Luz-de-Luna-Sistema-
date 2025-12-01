from django.shortcuts import render
from administracion.decorators import rol_requerido

@rol_requerido("Administrador","Empleado_Nivel1")
def submenu_reporteria(request):
    return render(request, "reporteria/Submenu.html")
