from datetime import timedelta, datetime
import secrets
import re

from django.utils import timezone
from django.utils.timezone import now, make_aware
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from django.views.generic.edit import FormView

from .models import Usuario, PasswordResetToken
from personal.models import Empleado
from .forms import ModificarMiUsuarioForm, RegistroUsuarioForm, LoginForm, EditarUsuarioForm
from .decorators import rol_requerido

User = get_user_model()


# ------------------ LOGIN ------------------
class LoginView(FormView):
    template_name = "administracion/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        # Limpiar mensajes previos
        list(messages.get_messages(request))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        # Verificar bloqueo previo
        block_until_ts = request.session.get("block_until")
        if block_until_ts:
            block_until = make_aware(datetime.fromtimestamp(block_until_ts))
            if now() < block_until:
                request.session["is_blocked"] = True
                messages.error(
                    request,
                    "Has superado el límite de intentos. Intenta de nuevo más tarde."
                )
                return self.form_invalid(form)
            else:
                # Bloqueo expirado
                request.session.pop("block_until", None)
                request.session["failed_attempts"] = 0
                request.session["is_blocked"] = False

        # Intento de login
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if not user or not check_password(password, user.password):
            # Usuario inexistente o contraseña incorrecta
            attempts = request.session.get("failed_attempts", 0) + 1
            request.session["failed_attempts"] = attempts

            if attempts >= 5:
                unblock_time = now() + timedelta(seconds=15)
                request.session["block_until"] = unblock_time.timestamp()
                request.session["is_blocked"] = True
                messages.error(
                    request,
                    "Cuenta bloqueada por intentos fallidos. Intenta de nuevo en 15 segundos."
                )
            else:
                request.session["is_blocked"] = False
                messages.error(request, "Usuario o contraseña incorrectos.")

            return self.form_invalid(form)

        # Usuario encontrado y contraseña correcta
        if not user.is_active:
            messages.error(request, "Usuario inactivo, contacte con el admin.")
            return self.form_invalid(form)

        # Login exitoso
        login(request, user)
        request.session["failed_attempts"] = 0
        request.session.pop("block_until", None)
        request.session["is_blocked"] = False
        return redirect("apps_home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_blocked"] = self.request.session.get("is_blocked", False)
        return context


def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------ DASHBOARD ------------------
@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def dashboard_admin(request):
    error = None
    usuarios = Usuario.objects.all()
    rol_filter = request.GET.get("rol", "")

    try:
        if rol_filter:
            usuarios = usuarios.filter(rol__nombre=rol_filter)
    except Exception:
        usuarios = []
        error = "Hubo un problema, por favor verifique su conexión, inténtelo de nuevo o vuelva a iniciar sesión"

    return render(request, "administracion/dashboard_admin.html", {
        "usuarios": usuarios,
        "error": error,
        "rol_filter": rol_filter
    })


# ------------------ PERFIL ------------------
@login_required
def perfil_empleado(request):
    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            cedula = form.cleaned_data.get("cedula")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")

            if cedula and (not cedula.isdigit() or len(cedula) != 9):
                form.add_error("cedula", "Formato de cédula inválido")

            if first_name and not first_name.isalpha():
                form.add_error("first_name", "Caracteres indebidos")
            if last_name and not last_name.isalpha():
                form.add_error("last_name", "Caracteres indebidos")

            if form.errors:
                return render(request, "administracion/perfil_empleado.html", {"form": form})

            form.save()
            messages.success(request, "Perfil actualizado correctamente")
            return redirect("perfil_empleado")
    else:
        form = EditarUsuarioForm(instance=request.user)

    return render(request, "administracion/perfil_empleado.html", {"form": form})


@login_required
def modificar_mi_usuario(request):
    usuario = request.user
    tiene_empleado = hasattr(usuario, 'empleado')

    if request.method == "POST":
        form = ModificarMiUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Información actualizada correctamente")
            return redirect("apps_home")
    else:
        form = ModificarMiUsuarioForm(instance=usuario)

    return render(request, "administracion/modificar_mi_usuario.html", {
        "form": form,
        "usuario": usuario,
        "tiene_empleado": tiene_empleado
    })


# ------------------ REGISTRO Y EDICIÓN DE USUARIOS ------------------
@rol_requerido("Administrador")
@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def registrar_usuario(request):
    mostrar_modal = False
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            mostrar_modal = True
            form = RegistroUsuarioForm()
    else:
        form = RegistroUsuarioForm()

    return render(request, "administracion/registro.html", {
        "form": form,
        "mostrar_modal": mostrar_modal
    })

@rol_requerido("Administrador")
@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def modificar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            cedula = form.cleaned_data.get("cedula")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")

            if cedula and (not cedula.isdigit() or len(cedula) != 9):
                form.add_error("cedula", "Formato de cédula inválido")
            if first_name and not first_name.isalpha():
                form.add_error("first_name", "Caracteres indebidos")
            if last_name and not last_name.isalpha():
                form.add_error("last_name", "Caracteres indebidos")

            if form.errors:
                return render(request, "administracion/modificar_usuario.html", {"form": form, "usuario": usuario})

            form.save()
            messages.success(request, "Modificación exitosa")
            return redirect("dashboard_admin")
    else:
        form = EditarUsuarioForm(instance=usuario)

    return render(request, "administracion/modificar_usuario.html", {"form": form, "usuario": usuario})

@rol_requerido("Administrador")
@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def activar_inactivar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.is_active = not usuario.is_active
    usuario.save()
    return redirect("dashboard_admin")


# ------------------ LINK USUARIO-EMPLEADO ------------------
@rol_requerido("Administrador")
@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def linkear_usuario_empleado(request):
    usuarios = Usuario.objects.all()
    empleados = Empleado.objects.all()
    if request.method == "POST":
        usuario_id = request.POST.get("usuario")
        empleado_id = request.POST.get("empleado")
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            empleado = Empleado.objects.get(id=empleado_id)
            empleado.usuario = usuario
            empleado.save()
            messages.success(request, "Linkeo exitoso")
            return redirect("linkear_usuario_empleado")
        except Exception as e:
            print(e)
            messages.error(request, "Hubo un problema al realizar el linkeo, por favor probar de nuevo")

    return render(request, "administracion/linkear_usuario_empleado.html", {
        "usuarios": usuarios,
        "empleados": empleados
    })


# ------------------ RESET DE CONTRASEÑA ------------------
@rol_requerido("Administrador")
@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def generar_reset_link(request, user_id):
    """Genera un token único y persistente en BD, devuelve el link como JSON."""
    try:
        usuario = Usuario.objects.get(id=user_id)
        token_obj = PasswordResetToken.crear_token(usuario)
        reset_link = request.build_absolute_uri(reverse('reset_password_view', args=[token_obj.token]))
        return JsonResponse({"link": reset_link})
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)


def reset_password_view(request, token):
    """Permite cambiar la contraseña si el token es válido y no expiró."""
    try:
        token_obj = PasswordResetToken.objects.get(token=token, usado=False)
    except PasswordResetToken.DoesNotExist:
        return render(request, "administracion/reset_password_invalid.html")

    if timezone.now() > token_obj.expira:
        token_obj.delete()
        return render(request, "administracion/reset_password_invalid.html")

    usuario = token_obj.usuario

    if request.method == "POST":
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        if not pass1 or not pass2:
            error = "Ambos campos son obligatorios."
        elif pass1 != pass2:
            error = "Las contraseñas no coinciden."
        elif len(pass1) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."
        elif not re.search(r"[A-Za-z]", pass1) or not re.search(r"[0-9]", pass1):
            error = "La contraseña debe contener letras y números."
        else:
            usuario.set_password(pass1)
            usuario.save()
            token_obj.usado = True
            token_obj.save()
            return render(request, "administracion/reset_password_success.html")

        return render(request, "administracion/reset_password.html", {
            "usuario": usuario,
            "token": token,
            "error": error
        })

    usuario.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, usuario)
    return render(request, "administracion/reset_password.html", {"usuario": usuario, "token": token})


# ------------------ APPS HOME ------------------
@login_required
def apps_home(request):
    user = request.user
    rol = user.rol.nombre if user.rol else None

    todas_las_apps = [
        {"name": "Administración", "url": "dashboard_admin", "id": "admin"},
        {"name": "Personal", "url": "marcar_asistencia", "id": "personal"},
        {"name": "Contabilidad", "url": "contabilidad_panel", "id": "contabilidad"},
        {"name": "Inventario", "url": "lista_inventario", "id": "inventario"},
        {"name": "Limpieza", "url": "index_limpieza", "id": "limpieza"},
        {"name": "Marketing", "url": "dashboard_marketing", "id": "marketing"},
        {"name": "Reportería", "url": "reporteria:submenu_reporteria", "id": "reporteria"},
        {"name": "Reservas", "url": "index_reservas", "id": "reservas"},
    ]

    if rol == "Administrador":
        apps = todas_las_apps 

    elif rol == "Empleado_Nivel1":
        apps = [app for app in todas_las_apps if app["id"] != "admin"]

    elif rol == "Empleado_Nivel2":
        permitidas = ["personal", "limpieza", "inventario", "reservas"]
        apps = [app for app in todas_las_apps if app["id"] in permitidas]

    else:
        apps = []

    return render(request, "administracion/apps_home.html", {"apps": apps})

