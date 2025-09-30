from django.shortcuts import render, get_object_or_404, redirect
from .forms import FiltroAsistenciaForm
from .models import Asistencia
from django.utils import timezone
from datetime import time, datetime, timedelta
from .models import Empleado, Asistencia, Rol, Pais, Provincia, Canton, Distrito, Direccion, Puesto
from .forms import EmpleadoForm, PuestoForm
from django.contrib import messages
from .forms import EmpleadoSeleccionForm

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
    empleados = Empleado.objects.filter(activo=True)
    puestos = Puesto.objects.filter(activo=True)  
    
    buscar = request.GET.get("buscar")  
    puesto_id = request.GET.get("puesto")

    if buscar:
        empleados = empleados.filter(nombre__icontains=buscar) | empleados.filter(apellido__icontains=buscar)

    if puesto_id:
        empleados = empleados.filter(puesto_id=puesto_id)

    context = {
        "empleados": empleados,
        "puestos": puestos,
        "puesto_id": puesto_id,
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
        empleado.save()
        messages.success(request, "Empleado inactivado satisfactoriamente")
    else:
        messages.info(request, "El empleado ya estaba inactivo")

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

def lista_puestos(request):
    query = request.GET.get('buscar')
    if query:
        puestos = Puesto.objects.filter(nombre__icontains=query, activo=True)
    else:
        puestos = Puesto.objects.filter(activo=True)
    return render(request, "personal/lista_puestos.html", {"puestos": puestos})



def agregar_puesto(request):
    if request.method == 'POST':
        form = PuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('puestos') 
    else:
        form = PuestoForm()

    datos = {
        'form': form
    }
    return render(request, 'personal/agregar_puesto.html', datos)


def editar_puesto(request, id):
    puesto = get_object_or_404(Puesto, id=id)

    if request.method == 'POST':
        form = PuestoForm(request.POST, instance=puesto)
        if form.is_valid():
            form.save()
            return redirect('puestos')
    else:
        form = PuestoForm(instance=puesto)

    datos = {
        'form': form,
        'puesto': puesto
    }
    return render(request, 'personal/editar_puesto.html', datos)


def eliminar_puesto(request, id):
    puesto = get_object_or_404(Puesto, id=id)
    puesto.delete()
    return redirect('puestos')

def inactivar_puesto(request, id):
    puesto = get_object_or_404(Puesto, id=id)

    if puesto.activo:
        puesto.activo = False
        puesto.save()
        messages.success(request, "Puesto inactivado satisfactoriamente")
    else:
        messages.info(request, "El puesto ya estaba inactivo")

    return redirect('puestos')

def visualizar_tiempos(request):
    empleados = Empleado.objects.filter(activo=True)
    puestos = Puesto.objects.filter(activo=True)

    fecha = request.GET.get("fecha")      # Usamos solo un campo "fecha"
    puesto_id = request.GET.get("puesto") # Filtrado por puesto

    asistencias = None  # Para que el template no truene si no hay datos

    if fecha:
        asistencias = Asistencia.objects.filter(fecha=fecha)
    else:
        asistencias = Asistencia.objects.all()

    if puesto_id:
        empleados = empleados.filter(puesto_id=puesto_id)
        asistencias = asistencias.filter(empleado__puesto_id=puesto_id)

    context = {
        "empleados": empleados,
        "puestos": puestos,
        "asistencias": asistencias,
        "fecha": fecha,
        "puesto_id": puesto_id,
    }
    return render(request, "personal/visualizar_tiempos.html", context)
