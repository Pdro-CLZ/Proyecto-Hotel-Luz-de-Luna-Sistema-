from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_inventario, name='lista_inventario'),
    path('crear/', views.crear_inventario, name='crear_inventario'),
    path('editar/<int:pk>/', views.editar_inventario, name='editar_inventario'),
    path('editar-cantidad/<int:pk>/', views.editar_cantidad_inventario, name='editar_cantidad_inventario'),
    path('activar-inactivar/<int:pk>/', views.activar_inactivar_inventario, name='activar_inactivar_inventario'),
]
