from django.urls import path
from . import views_finanzas, views_limpieza
from . import views_personal
from . import views_inventario 
app_name = "reporteria"

urlpatterns = [
    path("finanzas/", views_finanzas.reporte_financiero, name="reporte_financiero"),
    path('limpieza/', views_limpieza.reporte_limpieza, name='reporte_limpieza'),
    path("personal/", views_personal.reporte_personal, name="reporte_personal"),
    path('inventario/', views_inventario.reporte_inventario, name='reporte_inventario'),
]
