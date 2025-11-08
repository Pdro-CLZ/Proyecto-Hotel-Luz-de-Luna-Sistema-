from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacto/', views.contacto, name='contacto'),
    path('actividades/', views.actividades, name='actividades'),
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('login/', views.login_cliente, name='login_cliente'),
    path('activar/<uidb64>/<token>/', views.activar_usuario, name='activar_usuario'),
    path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', views.perfil, name='perfil_cliente'),  # opcional, si quieres mostrar perfil
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('consultar/', views.consultar_disponibilidad, name='consultar_disponibilidad'),
    path('reservar/<int:habitacion_id>/', views.reservar_habitacion, name='reservar_habitacion'),
]
