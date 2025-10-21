from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_limpieza, name='index_limpieza'),
    path('zonas/', views.lista_zonas, name='lista_zonas'),
    path('zonas/agregar/', views.registrar_zona, name='registrar_zona'),
    path('zonas/editar/<int:zona_id>/', views.editar_zona, name='editar_zona'),
]
