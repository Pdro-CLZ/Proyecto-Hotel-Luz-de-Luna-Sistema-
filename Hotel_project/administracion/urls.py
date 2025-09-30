from django.urls import path
from . import views
from .views import LoginView

urlpatterns = [
    path("mi-perfil/", views.modificar_mi_usuario, name="modificar_mi_usuario"),
    path('', views.apps_home, name='apps_home'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_admin, name="dashboard_admin"),
    path("perfil/", views.perfil_empleado, name="perfil_empleado"),
    path("registro/", views.registrar_usuario, name="registro"),
    path("modificar/<int:usuario_id>/", views.modificar_usuario, name="modificar_usuario"),
    path("activar/<int:usuario_id>/", views.activar_inactivar_usuario, name="activar_inactivar_usuario"),
]
