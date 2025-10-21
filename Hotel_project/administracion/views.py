from datetime import timedelta
import secrets

from django.utils import timezone
from django.utils.timezone import now, make_aware
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
import re 

from django.views.generic.edit import FormView

from .models import Usuario
from personal.models import Empleado
from .forms import ModificarMiUsuarioForm, RegistroUsuarioForm, LoginForm, EditarUsuarioForm

import datetime

User = get_user_model()

class LoginView(FormView):
    template_name = "administracion/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        list(messages.get_messages(request))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        # Revisar si está bloqueado
        block_until_ts = request.session.get("block_until")
        if block_until_ts:
            block_until = make_aware(datetime.fromtimestamp(block_until_ts))
            if now() < block_until:
                request.session["is_blocked"] = True
                messages.error(
                    request,
                    "Has superado el límite de intentos. Intenta de nuevo en 15 segundos."
                )
                return self.form_invalid(form)
            else:
                request.session.pop("block_until", None)
                request.session["failed_attempts"] = 0
                request.session["is_blocked"] = False

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            if not user.is_active:
                messages.error(request, "Usuario inactivo, por favor contacte con el admin.")
                return self.form_invalid(form)

            if check_password(password, user.password):
                login(request, user)
                request.session["failed_attempts"] = 0
                request.session.pop("block_until", None)
                request.session["is_blocked"] = False
                return redirect("apps_home")
            else:
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
                    messages.error(request, "Usuario o contraseña incorrectos.")
                    request.session["is_blocked"] = False

                return self.form_invalid(form)
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_blocked"] = self.request.session.get("is_blocked", False)
        return context


def logout_view(request):
    logout(request)
    return redirect("login")


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


@login_required
def perfil_empleado(request):
    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            # Validación solo de campos existentes
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


@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def activar_inactivar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.is_active = not usuario.is_active
    usuario.save()
    return redirect("dashboard_admin")


def apps_home(request):
    apps = [
        {"name": "Administración", "url": "dashboard_admin"},
        {"name": "Personal", "url": "marcar_asistencia"},
        {"name": "Contabilidad", "url": "contabilidad_panel"},
        {"name": "Inventario", "url": "lista_inventario"},
        {"name": "Limpieza", "url": "apps_home"},
        {"name": "Marketing", "url": "dashboard_marketing"},
        {"name": "Reportería", "url": "apps_home"},
        {"name": "Reservas", "url": "apps_home"},
    ]
    return render(request, "administracion/apps_home.html", {"apps": apps})


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


@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def linkear_usuario_empleado(request):
    usuarios = Usuario.objects.all()
    empleados = Empleado.objects.all()  # CORREGIDO: traer Empleados reales

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
    


# Diccionario temporal con tokens: {token: {"user_id": ..., "exp": ...}}
reset_tokens = {}

@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def generar_reset_link(request, user_id):
    """Genera un token único de un solo uso y devuelve el link como JSON."""
    try:
        usuario = Usuario.objects.get(id=user_id)
        token = secrets.token_urlsafe(16)
        # Expira en 10 minutos
        reset_tokens[token] = {"user_id": usuario.id, "exp": timezone.now() + datetime.timedelta(minutes=10)}
        reset_link = request.build_absolute_uri(reverse('reset_password_view', args=[token]))
        return JsonResponse({"link": reset_link})
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)


def reset_password_view(request, token):
    """Permite cambiar la contraseña si el token es válido y no expiró."""
    data = reset_tokens.get(token)
    if not data:
        return render(request, "administracion/reset_password_invalid.html")

    # Validar expiración
    if timezone.now() > data["exp"]:
        del reset_tokens[token]
        return render(request, "administracion/reset_password_invalid.html")

    usuario = Usuario.objects.get(id=data["user_id"])

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
            del reset_tokens[token]  # token de un solo uso
            return render(request, "administracion/reset_password_success.html")

        return render(request, "administracion/reset_password.html", {
            "usuario": usuario,
            "token": token,
            "error": error
        })

    # Inicia sesión automática solo durante el cambio
    usuario.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, usuario)
    return render(request, "administracion/reset_password.html", {"usuario": usuario, "token": token})




