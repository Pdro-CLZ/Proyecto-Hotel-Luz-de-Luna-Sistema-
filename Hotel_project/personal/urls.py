from django.urls import path
from . import views

urlpatterns = [
    path("", views.marcar_asistencia, name="marcar_asistencia"),

    path("empleados/", views.lista_empleados, name="empleados"),
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/inactivar/<int:id>/', views.inactivar_empleado, name='inactivar_empleado'),
    path("empleados/tiempos/", views.visualizar_tiempos, name="visualizar_tiempos"),
    path("empleados/seleccionar/", views.seleccionar_empleado, name="seleccionar_empleado"),




    path("puestos/", views.lista_puestos, name="puestos"),
    path("puestos/agregar/", views.agregar_puesto, name="agregar_puesto"),
    path("puestos/editar/<int:id>/", views.editar_puesto, name="editar_puesto"),
    path("puestos/inactivar/<int:id>/", views.inactivar_puesto, name="inactivar_puesto"),

]
