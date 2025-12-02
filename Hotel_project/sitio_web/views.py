from django.templatetags.static import static
from django.shortcuts import render, redirect,  get_object_or_404
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


from django.db.models import Sum
from reservas.models import Habitacion, FechaReservada, PrecioHabitacion, Reserva
from .forms import ConsultaDisponibilidadForm

import os

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

from django.db.models import Sum
from django.shortcuts import render
from reservas.models import Habitacion, FechaReservada, PrecioHabitacion
from .forms import ConsultaDisponibilidadForm
from .models import Amenidad

def consultar_disponibilidad(request):
    habitaciones_disponibles = []
    precios_totales = {}

    if request.method == 'POST':
        form = ConsultaDisponibilidadForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            request.session['fecha_inicio'] = str(fecha_inicio)
            request.session['fecha_fin'] = str(fecha_fin)

            habitaciones_ocupadas = FechaReservada.objects.filter(
                fecha__range=(fecha_inicio, fecha_fin)
            ).values_list('habitacion_id', flat=True).distinct()

            habitaciones_disponibles = Habitacion.objects.exclude(
                id__in=habitaciones_ocupadas
            ).prefetch_related('amenidades')

            busqueda = request.POST.get("busqueda", "").strip()

            if busqueda:
                habitaciones_disponibles = habitaciones_disponibles.filter(
                    nombre__icontains=busqueda
                )

            for hab in habitaciones_disponibles:
                total = PrecioHabitacion.objects.filter(
                    habitacion=hab,
                    fecha__range=(fecha_inicio, fecha_fin)
                ).aggregate(total=Sum('precio'))['total'] or 0
                precios_totales[hab.id] = total

    else:
        form = ConsultaDisponibilidadForm()

    amenidades = Amenidad.objects.all()
    context = {
        'form': form,
        'habitaciones_disponibles': habitaciones_disponibles,
        'precios_totales': precios_totales,
        'amenidades': amenidades,
    }

    return render(request, 'sitio_web/consultar_disponibilidad.html', context)


from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from reservas.models import Habitacion, Reserva, Cliente

# sitio_web/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from reservas.models import Habitacion, PrecioHabitacion

def reservar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)

    fecha_inicio = request.session.get('fecha_inicio')
    fecha_fin = request.session.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        messages.error(request, "Debes seleccionar un rango de fechas antes de reservar.")
        return redirect('consultar_disponibilidad')

    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        cedula = request.POST.get('cedula', '').strip()

        errores = []

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]{3,}$', nombre):
            errores.append("El nombre debe tener al menos 3 letras y solo contener caracteres alfabéticos.")

        try:
            validate_email(correo)
        except ValidationError:
            errores.append("El correo electrónico no es válido.")

        if not re.match(r'^\d{8}$', telefono):
            errores.append("El número de teléfono debe tener exactamente 8 dígitos.")

        if not re.match(r'^\d{9}$', cedula):
            errores.append("La cédula debe tener exactamente 9 dígitos.")

        if errores:
            for e in errores:
                messages.error(request, e)
        else:
            # Guardamos datos en sesión para crear reserva después del pago
            request.session['cliente_datos'] = {
                "nombre": nombre,
                "correo": correo,
                "telefono": telefono,
                "cedula": cedula,
            }
            request.session['habitacion_id'] = habitacion.id

            return redirect('crear_pago_paypal')

    return render(request, 'sitio_web/form_reserva.html', {'habitacion': habitacion})

import paypalrestsdk
from django.shortcuts import redirect
from django.conf import settings
from reservas.models import Habitacion, PrecioHabitacion
from datetime import datetime

def crear_pago_paypal(request):
    cliente = request.session.get("cliente_datos")
    habitacion_id = request.session.get("habitacion_id")
    fecha_inicio = request.session.get("fecha_inicio")
    fecha_fin = request.session.get("fecha_fin")

    if not cliente or not habitacion_id:
        messages.error(request, "Debe completar el formulario de reserva.")
        return redirect('consultar_disponibilidad')

    habitacion = Habitacion.objects.get(id=habitacion_id)

    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    # Calcular total
    total_qs = PrecioHabitacion.objects.filter(
        habitacion=habitacion,
        fecha__range=(fecha_inicio, fecha_fin)
    ).aggregate(total=models.Sum('precio'))

    total = total_qs['total'] or 0

    # Crear pago PayPal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": { "payment_method": "paypal" },
        "redirect_urls": {
            "return_url": request.build_absolute_uri("/sitio/paypal/success/"), 
            "cancel_url": request.build_absolute_uri("/sitio/paypal/cancel/")
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"Reserva Habitación {habitacion.nombre}",
                    "sku": "ReservaHotel",
                    "price": f"{total:.2f}",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": { "total": f"{total:.2f}", "currency": "USD" },
            "description": "Pago de reserva en el hotel."
        }]
    })

    if payment.create():
        # Buscar y redirigir a PayPal
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        messages.error(request, "Error creando pago con PayPal.")
        return redirect('consultar_disponibilidad')

from django.shortcuts import render
from reservas.models import Reserva, Cliente, FechaReservada
from datetime import timedelta
from django.core.mail import send_mail

def paypal_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if not payment.execute({"payer_id": payer_id}):
        return render(request, "sitio_web/error_pago.html")

    # Recuperar datos guardados
    cliente_datos = request.session.get('cliente_datos')
    habitacion_id = request.session.get('habitacion_id')
    fecha_inicio = datetime.strptime(request.session['fecha_inicio'], "%Y-%m-%d").date()
    fecha_fin = datetime.strptime(request.session['fecha_fin'], "%Y-%m-%d").date()

    habitacion = Habitacion.objects.get(id=habitacion_id)

    # Crear o recuperar cliente
    cliente, _ = Cliente.objects.get_or_create(
        identificacion=cliente_datos["cedula"],
        defaults={
            "nombre": cliente_datos["nombre"],
            "apellido": "",
            "telefono": cliente_datos["telefono"],
            "correo": cliente_datos["correo"]
        }
    )

    # Calcular total
    precios = PrecioHabitacion.objects.filter(
        habitacion=habitacion,
        fecha__range=(fecha_inicio, fecha_fin)
    ).aggregate(total=models.Sum('precio'))

    total = precios["total"] or 0

    # Crear reserva real
    reserva = Reserva.objects.create(
        habitacion=habitacion,
        cliente=cliente,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        total=total,
        metodo_pago="tarjeta",
        canal_reservacion="sitio"
    )

    # Registrar cada día
    dia = fecha_inicio
    while dia <= fecha_fin:
        FechaReservada.objects.create(
            habitacion=habitacion,
            fecha=dia,
            reserva=reserva
        )
        dia += timedelta(days=1)

    # Enviar correo
    send_mail(
        "Confirmación de Reserva",
        f"Tu reserva del {fecha_inicio} al {fecha_fin} ha sido confirmada.",
        None,
        [cliente.correo],
        fail_silently=True
    )

    return render(request, "sitio_web/reserva_confirmada.html", {"reserva": reserva})

# sitio_web/views.py

from django.shortcuts import render, redirect
from django.contrib import messages # Asegúrate de importar esto

def paypal_cancel(request):
    """
    Muestra la página de cancelación después de que el usuario cancela el pago
    en la pasarela de PayPal.
    """
    
    # 1. Mostrar un mensaje al usuario
    messages.warning(request, "El proceso de pago fue cancelado. No se realizó ningún cargo.")
    
    # 2. (Opcional pero recomendado) Limpiar datos sensibles de la sesión 
    #    para evitar que se intenten usar en procesos futuros no deseados.
    if 'cliente_datos' in request.session:
        del request.session['cliente_datos']
    if 'habitacion_id' in request.session:
        del request.session['habitacion_id']
    if 'fecha_inicio' in request.session:
        del request.session['fecha_inicio']
    if 'fecha_fin' in request.session:
        del request.session['fecha_fin']
        
    # 3. Renderizar el template de cancelación
    return render(request, "sitio_web/cancelado.html")


def reserva_confirmada(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'sitio_web/reserva_confirmada.html', {'reserva': reserva})



def detalle_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    precios = PrecioHabitacion.objects.filter(habitacion=habitacion).order_by('fecha')
    from django.template.loader import select_template

    template_names = [f'sitio_web/detalle_habitacion_{habitacion.id}.html', 'sitio_web/detalle_habitacion.html']
    template = select_template(template_names)

    return render(request, template.template.name, {
        'habitacion': habitacion,
        'precios': precios
    })


def set_language(request, lang):
    """Set `site_lang` in session (only for sitio_web module) and redirect back."""
    from django.urls import reverse
    from django.conf import settings

    available = [c for c, _ in getattr(settings, 'LANGUAGES', [])]
    if lang not in available:
        lang = getattr(settings, 'LANGUAGE_CODE', 'es')

    request.session['site_lang'] = lang

    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER')
    if not next_url:
        try:
            next_url = reverse('index')
        except Exception:
            next_url = '/'

    return redirect(next_url)


def habitaciones(request):
    habitaciones_list = Habitacion.objects.all().prefetch_related('amenidades')
    
    for hab in habitaciones_list:
        amenidades_nombres = [a.nombre.lower() for a in hab.amenidades.all()]
        
        if 'cama grande' in amenidades_nombres:
            hab.capacidad = 4
            hab.tipo_cama = 'Cama grande'
        else:
            hab.capacidad = 3
            hab.tipo_cama = 'Cama pequeña'
        
        hab.tiene_piscina = 'piscina' in amenidades_nombres
    
    return render(request, 'sitio_web/habitaciones.html', {'habitaciones': habitaciones_list})

def index(request):
    habitaciones_list = Habitacion.objects.all().prefetch_related('amenidades')[:4]
    
    for hab in habitaciones_list:
        amenidades_nombres = [a.nombre.lower() for a in hab.amenidades.all()]
        
        if 'cama grande' in amenidades_nombres:
            hab.capacidad = 4
            hab.tipo_cama = 'Cama grande'
        else:
            hab.capacidad = 3
            hab.tipo_cama = 'Cama pequeña'
        
        hab.tiene_piscina = 'piscina' in amenidades_nombres
    
    return render(request, 'sitio_web/index.html', {'habitaciones': habitaciones_list})

