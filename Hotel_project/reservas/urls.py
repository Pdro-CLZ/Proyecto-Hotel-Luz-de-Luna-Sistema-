from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_reservas, name='index_reservas'),
    path('agregar/', views.agregar_reserva, name='agregar_reserva'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('nueva_reserva_cliente/<int:habitacion_id>/<str:fecha_inicio>/<str:fecha_fin>/<int:cliente_id>/', views.nueva_reserva_cliente, name='nueva_reserva_cliente'),
    path('nueva_reserva_cliente/<int:habitacion_id>/<str:fecha_inicio>/<str:fecha_fin>/', views.nueva_reserva_cliente, name='nueva_reserva_cliente'),
    path('confirmar_reserva/<int:habitacion_id>/<str:fecha_inicio>/<str:fecha_fin>/<int:cliente_id>/<str:metodo_pago>/<str:canal_reservacion>/', views.confirmar_reserva, name='confirmar_reserva'),
    path("precios/", views.precios_calendario, name="precios_calendario"),
    path("precios/asignar/", views.asignar_precio_rango, name="asignar_precio_rango"),

]