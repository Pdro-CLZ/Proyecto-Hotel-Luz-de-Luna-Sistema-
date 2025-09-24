from django.urls import path
from . import views
from .views import LoginView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_admin, name="dashboard_admin"),
    path("perfil/", views.perfil_empleado, name="perfil_empleado"),
    path("registro/", views.registrar_usuario, name="registro"),
    path("modificar/<int:usuario_id>/", views.modificar_usuario, name="modificar_usuario"),
    path("activar/<int:usuario_id>/", views.activar_inactivar_usuario, name="activar_inactivar_usuario"),
]
