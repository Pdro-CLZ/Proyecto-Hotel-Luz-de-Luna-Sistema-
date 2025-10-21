from django.urls import path
from . import views

urlpatterns = [
    path('', views.contabilidad_panel, name='contabilidad_panel'),
    path('agregar_ingreso/', views.agregar_ingreso, name='agregar_ingreso'),
    path('agregar_gasto/', views.agregar_gasto, name='agregar_gasto'),
    path('editar_ingreso/<int:id>/', views.editar_ingreso, name='editar_ingreso'),
    path('editar_gasto/<int:id>/', views.editar_gasto, name='editar_gasto'),
    path('cierre_mensual/', views.cierre_mensual, name='cierre_mensual'),
    path('cierre_anual/', views.cierre_anual, name='cierre_anual'),

]
