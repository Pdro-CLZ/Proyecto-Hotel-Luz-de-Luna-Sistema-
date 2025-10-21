from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_marketing, name='dashboard_marketing'),
    path('plantillas/', views.lista_plantillas, name='lista_plantillas'),
    path('plantillas/crear/', views.crear_plantilla, name='crear_plantilla'),
    path('plantillas/editar/<int:pk>/', views.editar_plantilla, name='editar_plantilla'),
    path('plantillas/eliminar/<int:pk>/', views.eliminar_plantilla, name='eliminar_plantilla'),
    path('campania/', views.crear_campania, name='crear_campania'),
]
