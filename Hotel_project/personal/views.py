from django.shortcuts import render, get_object_or_404, redirect
from .forms import FiltroAsistenciaForm
from .models import Asistencia
from django.utils import timezone
from datetime import time, datetime, timedelta
from .models import Empleado, Asistencia, Rol, Pais, Provincia, Canton, Distrito, Direccion
from .forms import EmpleadoForm
from administracion.forms import RolForm
from django.contrib import messages
from .forms import EmpleadoSeleccionForm
from django.db.models import Q 

# Create your views here.
def marcar_asistencia(request):
    empleado_id = 1 # Cambiar cuando se implemente la logica de login
    empleado = get_object_or_404(Empleado, pk=empleado_id)

    fecha_actual = timezone.localdate()
    asistencia, created = Asistencia.objects.get_or_create(empleado=empleado, fecha=fecha_actual)
    mensaje = None

    if request.method == "POST" and request.POST.get("action") == "llegada":
        now = timezone.localtime()
        now_time = now.time()

        if asistencia.hora_salida:
            mensaje = f"Hora de salida ya registrada: {asistencia.hora_salida.strftime('%H:%M:%S')}, NO se puede registrar hora de entrada, por favor comunicarse con el administrador"
        else:
            if asistencia.hora_llegada:
                mensaje = f"Hora de llegada ya registrada: {asistencia.hora_llegada.strftime('%H:%M:%S')}"
            else: 
                asistencia.hora_llegada = now_time

                if (now_time >= time(19, 0)) or (now_time <= time(5, 30)):
                    asistencia.observaciones = "Hora de llegada inusual, por favor comunicarse con el administrador"
                    mensaje = asistencia.observaciones
                else:
                    asistencia.observaciones = "Registro Añadido Correctamente"
                    mensaje = asistencia.observaciones
                
                asistencia.save()

    if request.method == "POST" and request.POST.get("action") == "salida":
        now = timezone.localtime()
        now_time = now.time()

        if asistencia.hora_salida:
            mensaje = f"Hora de salida ya registrada: {asistencia.hora_salida.strftime('%H:%M:%S')}"
        else: 
            asistencia.hora_salida = now_time

            if asistencia.hora_llegada: 
                hora_llegada_dt = datetime.combine(asistencia.fecha, asistencia.hora_llegada)
                hora_salida_dt = datetime.combine(asistencia.fecha, asistencia.hora_salida)
                total_horas = hora_salida_dt - hora_llegada_dt

                horas_trabajadas = total_horas.total_seconds() / 3600
                asistencia.horas_trabajadas = horas_trabajadas

                if total_horas < timedelta(hours=1):
                    asistencia.observaciones = "Hora de salida inusual, por favor comunicarse con el administrador"
                    mensaje = asistencia.observaciones

                else:
                    asistencia.observaciones = "Registro Añadido Correctamente"
                    mensaje = asistencia.observaciones
            else:
                    asistencia.observaciones = "No hay hora de llegada registrada, por favor comunicarse con el administrador"
                    mensaje = asistencia.observaciones
                    
            asistencia.save()
    
    hora_marca_ingreso = asistencia.hora_llegada.strftime("%H:%M:%S") if asistencia.hora_llegada else "No registrada"
    hora_marca_salida = asistencia.hora_salida.strftime("%H:%M:%S") if asistencia.hora_salida else "No registrada"

    datos = {
        "empleado": empleado,
        "mensaje": mensaje,
        "hora_marca_ingreso": hora_marca_ingreso,
        "hora_marca_salida": hora_marca_salida,
    }
    return render(request, "personal/index.html", datos)


def lista_empleados(request):
    empleados = Empleado.objects.all()
    roles = Rol.objects.all()

    # Filtro por búsqueda
    buscar = request.GET.get("buscar")
    if buscar:
        empleados = empleados.filter(
            Q(nombre__icontains=buscar) |
            Q(apellido__icontains=buscar) |
            Q(cedula__icontains=buscar)
        )

    # Filtro por rol
    rol_id = request.GET.get("rol")
    if rol_id:
        empleados = empleados.filter(rol_id=rol_id)

    # Filtro por estado (activo/inactivo)
    estado = request.GET.get("estado")
    if estado == "1":  # Activos
        empleados = empleados.filter(activo=True)
    elif estado == "0":  # Inactivos
        empleados = empleados.filter(activo=False)

    context = {
        "empleados": empleados,
        "roles": roles,
        "rol_id": rol_id,
        "estado": estado,
    }
    return render(request, "personal/lista_empleados.html", context)




def agregar_empleado(request):
    roles = Rol.objects.all()
    paises = Pais.objects.all()
    provincias = Provincia.objects.all()
    cantones = Canton.objects.all()
    distritos = Distrito.objects.all()

    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)

            direccion = Direccion.objects.create(
                direccion_exacta=request.POST['direccion_exacta'],
                pais_id=request.POST['pais'],
                provincia_id=request.POST['provincia'],
                canton_id=request.POST['canton'],
                distrito_id=request.POST['distrito']
            )
            empleado.direccion = direccion
            empleado.save()
            return redirect('empleados') 
    else:
        form = EmpleadoForm()

    datos = {
        'form': form,
        'roles': roles,
        'paises': paises,
        'provincias': provincias,
        'cantones': cantones,
        'distritos': distritos,
    }
    return render(request, 'personal/agregar_empleado.html', datos)


def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    roles = Rol.objects.all()
    paises = Pais.objects.all()
    provincias = Provincia.objects.all()
    cantones = Canton.objects.all()
    distritos = Distrito.objects.all()

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            empleado = form.save(commit=False)

            direccion = empleado.direccion
            direccion.direccion_exacta = request.POST['direccion_exacta']
            direccion.pais_id = request.POST['pais']
            direccion.provincia_id = request.POST['provincia']
            direccion.canton_id = request.POST['canton']
            direccion.distrito_id = request.POST['distrito']
            direccion.save()

            empleado.save()
            return redirect('empleados')
    else:
        form = EmpleadoForm(instance=empleado)

    datos = {
        'form': form,
        'empleado': empleado,
        'roles': roles,
        'paises': paises,
        'provincias': provincias,
        'cantones': cantones,
        'distritos': distritos,
    }
    return render(request, 'personal/editar_empleado.html', datos)


def inactivar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)

    if empleado.activo:
        empleado.activo = False
        messages.success(request, f"Empleado {empleado.nombre} inactivado satisfactoriamente")
    else:
        empleado.activo = True
        messages.success(request, f"Empleado {empleado.nombre} activado satisfactoriamente")

    empleado.save()
    return redirect('empleados')


def seleccionar_empleado(request):
    if request.method == "POST":
        form = EmpleadoSeleccionForm(request.POST)
        if form.is_valid():
            empleado = form.cleaned_data['empleado']
            # Redirigir a la página de edición del empleado seleccionado
            return redirect('editar_empleado', id=empleado.id)
        else:
            mensaje = "Por favor escoja un ID"
    else:
        form = EmpleadoSeleccionForm()
        mensaje = None

    return render(request, "personal/seleccionar_empleado.html", {"form": form, "mensaje": mensaje})

def lista_roles(request):
    query = request.GET.get('buscar')
    estado = request.GET.get("estado")

    roles = Rol.objects.all()

    if query:
        roles = roles.filter(nombre__icontains=query)
    if estado == "1":
        roles = roles.filter(activo=True)
    elif estado == "0":
        roles = roles.filter(activo=False)
    return render(request, "personal/lista_roles.html", {
        "roles": roles,
        "query": query,
        "estado": estado,
    })


def agregar_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles') 
    else:
        form = RolForm()

    datos = {
        'form': form
    }
    return render(request, 'personal/agregar_rol.html', datos)


def editar_rol(request, id):
    rol = get_object_or_404(Rol, id=id)

    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('roles')
    else:
        form = RolForm(instance=rol)

    datos = {
        'form': form,
        'rol': rol
    }
    return render(request, 'personal/editar_rol.html', datos)


def eliminar_rol(request, id):
    rol = get_object_or_404(Rol, id=id)
    rol.delete()
    return redirect('roles')


def inactivar_rol(request, id):
    rol = get_object_or_404(Rol, id=id)

    if rol.activo:
        rol.activo = False
        messages.success(request, f"Rol {rol.nombre} inactivado satisfactoriamente")
    else:
        rol.activo = True
        messages.success(request, f"Rol {rol.nombre} activado satisfactoriamente")

    rol.save()
    return redirect('roles')


def visualizar_tiempos(request):
    empleados = Empleado.objects.filter(activo=True)
    roles = Rol.objects.filter(activo=True)

    fecha = request.GET.get("fecha")      # Usamos solo un campo "fecha"
    rol_id = request.GET.get("rol") # Filtrado por rol

    asistencias = None  # Para que el template no truene si no hay datos

    if fecha:
        asistencias = Asistencia.objects.filter(fecha=fecha)
    else:
        asistencias = Asistencia.objects.all()

    if rol_id:
        empleados = empleados.filter(rol_id=rol_id)
        asistencias = asistencias.filter(empleado__rol_id=rol_id)

    context = {
        "empleados": empleados,
        "roles": roles,
        "asistencias": asistencias,
        "fecha": fecha,
        "rol_id": rol_id,
    }
    return render(request, "personal/visualizar_tiempos.html", context)
