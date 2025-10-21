from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from administracion.models import Rol, Usuario
from personal.models import Direccion, Pais, Provincia, Canton, Distrito
from sitio_web.models import Cliente
from .forms import RegistroClienteForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from sitio_web.forms import EditarPerfilForm

# Para envío de correo
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import get_user_model

@transaction.atomic
def registro_cliente(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():

            # Rol de cliente
            rol_cliente, _ = Rol.objects.get_or_create(
                nombre="Cliente",
                defaults={"descripcion": "Rol de cliente"}
            )

            # Generar username único
            base_username = f"{form.cleaned_data['nombre'].lower()}.{form.cleaned_data['apellido'].lower()}"
            username = base_username
            contador = 1
            while Usuario.objects.filter(username=username).exists():
                username = f"{base_username}{contador}"
                contador += 1

            # Crear usuario
            usuario = Usuario(
                username=username,
                email=form.cleaned_data["email"],
                cedula=form.cleaned_data["cedula"],
                first_name=form.cleaned_data["nombre"],
                last_name=form.cleaned_data["apellido"],  
                rol=rol_cliente,
                is_active=False,
            )
            usuario.set_password(form.cleaned_data["password1"])
            usuario.save()

            # Crear dirección
            pais_obj, _ = Pais.objects.get_or_create(nombre=form.cleaned_data["pais"])
            provincia_obj, _ = Provincia.objects.get_or_create(nombre=form.cleaned_data["provincia"])
            canton_obj, _ = Canton.objects.get_or_create(nombre=form.cleaned_data["canton"])
            distrito_obj, _ = Distrito.objects.get_or_create(nombre=form.cleaned_data["distrito"])

            direccion = Direccion.objects.create(
                direccion_exacta=form.cleaned_data["direccion_exacta"],
                pais=pais_obj,
                provincia=provincia_obj,
                canton=canton_obj,
                distrito=distrito_obj
            )

            # Crear cliente
            Cliente.objects.create(
                usuario=usuario,
                direccion=direccion,
                telefono=form.cleaned_data["telefono"],
                activo=True
            )

            # Generar token y link de activación
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            token = default_token_generator.make_token(usuario)
            activation_link = request.build_absolute_uri(
                reverse('activar_usuario', kwargs={'uidb64': uid, 'token': token})  
            )
            print("LINK DE ACTIVACIÓN:", activation_link)


            # Enviar correo inmediatamente a consola
            print("EMAIL_BACKEND ACTUAL:", settings.EMAIL_BACKEND)
            send_mail(
                'Confirma tu correo',
                f'Hola {form.cleaned_data["nombre"]}, confirma tu correo dando clic aquí: {activation_link}',
                settings.DEFAULT_FROM_EMAIL,  # usa DEFAULT_FROM_EMAIL
                [usuario.email],
                fail_silently=False,
            )
            print(">>> Correo enviado (o al menos intentado)")

            # Mostrar plantilla de confirmación
            return render(request, "sitio_web/confirmacion_registro.html", {
                "email": usuario.email
            })

        else:
            print(form.errors)
            messages.error(request, "Por favor corrige los errores en el formulario.")

    else:
        form = RegistroClienteForm()

    return render(request, "sitio_web/registro_cliente.html", {"form": form})


def activar_usuario(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None

    if usuario and default_token_generator.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()

        # Iniciar sesión automáticamente
        login(request, usuario)
        messages.success(request, f"¡Correo verificado, bienvenid@ {usuario.first_name}!")

        return redirect("index")
    else:
        messages.error(request, "El enlace de verificación no es válido o ha expirado.")
        return redirect("registro_cliente")



# Otras vistas
def index(request):
    return render(request, 'sitio_web/index.html')

def contacto(request):
    return render(request, 'sitio_web/contacto.html')

def actividades(request):
    return render(request, 'sitio_web/actividades.html')

def login_cliente(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "No se permite campos vacíos")
            return render(request, "sitio_web/login_cliente.html")

        try:
            usuario_obj = Usuario.objects.get(email=email)
            usuario = authenticate(request, username=usuario_obj.username, password=password)
        except Usuario.DoesNotExist:
            usuario = None

        if usuario is not None:
            login(request, usuario)
            messages.success(request, f"Bienvenid@ {usuario.username}!")
            return redirect("index")
        else:
            messages.error(request, "Correo o contraseña incorrecta")

    return render(request, "sitio_web/login_cliente.html")

def cerrar_sesion(request):
    # Cerrar sesión
    logout(request)

    # Limpiar mensajes antiguos
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # Esto vacía todos los mensajes previos

    # Agregar el mensaje correcto
    messages.success(request, "Has cerrado sesión correctamente.")

    # Redirigir al login
    return redirect("login_cliente")


@login_required
def perfil(request):
    return render(request, "sitio_web/perfil_cliente.html", {"usuario": request.user})

@login_required
def editar_perfil(request):
    usuario = request.user
    if request.method == "POST":
        form = EditarPerfilForm(request.POST, usuario=usuario)
        if form.is_valid():
            # Actualizar datos del usuario
            usuario.first_name = form.cleaned_data['nombre']
            usuario.last_name = form.cleaned_data['apellido']
            usuario.email = form.cleaned_data['email']
            usuario.save()

            # Actualizar dirección
            pais_obj, _ = Pais.objects.get_or_create(nombre=form.cleaned_data['pais'])
            provincia_obj, _ = Provincia.objects.get_or_create(nombre=form.cleaned_data['provincia'])
            canton_obj, _ = Canton.objects.get_or_create(nombre=form.cleaned_data['canton'])
            distrito_obj, _ = Distrito.objects.get_or_create(nombre=form.cleaned_data['distrito'])

            direccion = usuario.cliente.direccion
            direccion.direccion_exacta = form.cleaned_data['direccion_exacta']
            direccion.pais = pais_obj
            direccion.provincia = provincia_obj
            direccion.canton = canton_obj
            direccion.distrito = distrito_obj
            direccion.save()

            # Actualizar teléfono
            usuario.cliente.telefono = form.cleaned_data['telefono']
            usuario.cliente.save()

            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil_cliente')
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = EditarPerfilForm(usuario=usuario)

    return render(request, 'sitio_web/editar_perfil.html', {'form': form})