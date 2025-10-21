from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_limpieza, name='index_limpieza'),
    path('zonas/', views.lista_zonas, name='lista_zonas'),
    path('zonas/agregar/', views.registrar_zona, name='registrar_zona'),
    path('zonas/editar/<int:zona_id>/', views.editar_zona, name='editar_zona'),
    path('zonas/estado/', views.lista_zonas_empleado, name='lista_zonas_empleado'),
    path('zonas/<int:zona_id>/gestionar/', views.gestionar_zona, name='gestionar_zona'),
    path('zonas/tareas/<int:tarea_id>/cambiar_estado/', views.cambiar_estado_tarea, name='cambiar_estado_tarea'),
]
