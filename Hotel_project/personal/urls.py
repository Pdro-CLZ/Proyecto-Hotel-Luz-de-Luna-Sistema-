from django.urls import path
from . import views

urlpatterns = [
    path("", views.marcar_asistencia, name="marcar_asistencia"),

    path("empleados/", views.lista_empleados, name="empleados"),
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),

    path("puestos/", views.lista_puestos, name="puestos"),
    path("puestos/agregar/", views.agregar_puesto, name="agregar_puesto"),
    path("puestos/editar/<int:id>/", views.editar_puesto, name="editar_puesto"),
    path("puestos/eliminar/<int:id>/", views.eliminar_puesto, name="eliminar_puesto"),
]
