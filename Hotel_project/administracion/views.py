from datetime import datetime, timedelta  # datetime y timedelta de la librería estándar
from django.utils.timezone import now, make_aware  # now y make_aware de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import FormView

from .models import Usuario
from .forms import RegistroUsuarioForm, LoginForm, EditarUsuarioForm


class LoginView(FormView):
    template_name = "administracion/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        # Revisar si está bloqueado
        block_until_ts = request.session.get("block_until")
        is_blocked = False
        if block_until_ts:
            block_until = make_aware(datetime.fromtimestamp(block_until_ts))
            if now() < block_until:
                is_blocked = True
                messages.error(
                    request,
                    "Has superado el límite de intentos. Intenta de nuevo en 15 segundos."
                )
                request.session["is_blocked"] = True
                return self.form_invalid(form)
            else:
                # tiempo de bloqueo pasado, desbloquear
                request.session.pop("block_until", None)
                request.session["failed_attempts"] = 0
                request.session["is_blocked"] = False

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if request.session.get("is_blocked", False):
                messages.error(
                    request,
                    "Cuenta temporalmente bloqueada, espera antes de intentar."
                )
                return self.form_invalid(form)

            login(request, user)
            request.session["failed_attempts"] = 0
            request.session.pop("block_until", None)
            request.session["is_blocked"] = False
            return redirect("dashboard_admin")
        else:
            # Credenciales incorrectas
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Variable para frontend que controla el botón dinámico
        context["is_blocked"] = self.request.session.get("is_blocked", False)
        return context


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def dashboard_admin(request):
    usuarios = Usuario.objects.all()
    return render(request, "administracion/dashboard_admin.html", {"usuarios": usuarios})

@login_required
def perfil_empleado(request):
    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente")
            return redirect("perfil_empleado")
    else:
        form = EditarUsuarioForm(instance=request.user)
    return render(request, "administracion/perfil_empleado.html", {"form": form})

@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente")
            return redirect("dashboard_admin")
    else:
        form = RegistroUsuarioForm()
    return render(request, "administracion/registro.html", {"form": form})

@login_required
@user_passes_test(lambda u: u.rol and u.rol.nombre == "Administrador")
def modificar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            # Validaciones personalizadas
            telefono = form.cleaned_data["telefono"]
            cedula = form.cleaned_data["cedula"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            # Teléfono solo números y 8 dígitos
            if not telefono.isdigit() or len(telefono) != 8:
                form.add_error("telefono", "Teléfono con cantidad de números indebida o caracteres inválidos")

            # Cedula solo números y longitud 9
            if not cedula.isdigit() or len(cedula) != 9:
                form.add_error("cedula", "Formato de cédula inválido")

            # Nombre y apellido sin números ni caracteres especiales
            if not first_name.isalpha():
                form.add_error("first_name", "Caracteres indebidos")
            if not last_name.isalpha():
                form.add_error("last_name", "Caracteres indebidos")

            if form.errors:
                return render(request, "administracion/modificar_usuario.html", {"form": form, "usuario": usuario})

            # Guardar cambios si todo ok
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
