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




    path("roles/", views.lista_roles, name="roles"),
    path("roles/agregar/", views.agregar_rol, name="agregar_rol"),
    path("roles/editar/<int:id>/", views.editar_rol, name="editar_rol"),
    path("roles/inactivar/<int:id>/", views.inactivar_rol, name="inactivar_rol"),

]
