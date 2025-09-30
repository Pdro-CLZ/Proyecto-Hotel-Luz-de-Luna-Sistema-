from django.urls import path
from . import views

app_name = "limpieza" 

urlpatterns = [
    path("visualizar/", views.visualizar_estados, name="visualizar_estados"),
    path("registrar/<int:habitacion_id>/", views.registrar_estado, name="registrar_estado"),
    path("detalle/<int:habitacion_id>/", views.visualizar_estado, name="visualizar_estado"),
    path("registrar_zona/", views.registrar_zona, name="registrar_zona"),
    path("actualizar_zona/<int:zona_id>/", views.actualizar_zona, name="actualizar_zona"),

]
