from django.urls import path
from . import views_finanzas, views_limpieza
from . import views_personal
from . import views_inventario 
from . import views_reservas
from . import views_submenu 
app_name = "reporteria"

urlpatterns = [
    path("", views_submenu.submenu_reporteria, name="submenu_reporteria"),

    path("finanzas/", views_finanzas.reporte_financiero, name="reporte_financiero"),
    path('limpieza/', views_limpieza.reporte_limpieza, name='reporte_limpieza'),
    path("personal/", views_personal.reporte_personal, name="reporte_personal"),
    path('inventario/', views_inventario.reporte_inventario, name='reporte_inventario'),
    path('reservas/', views_reservas.reporte_reservas, name='reporte_reservas'),
]
