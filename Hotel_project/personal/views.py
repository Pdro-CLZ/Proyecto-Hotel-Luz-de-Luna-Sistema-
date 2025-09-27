from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import time, datetime, timedelta
from .models import Empleado, Asistencia, Rol, Pais, Provincia, Canton, Distrito, Direccion
from .forms import EmpleadoForm

# Create your views here.
def marcar_asistencia(request):
    empleado_id = 2 # Cambiar cuando se implemente la logica de login
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
    return render(request, "index.html", datos)


def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, "lista_empleados.html", {"empleados": empleados})


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
            return redirect('/personal/empleados') 
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
    return render(request, 'agregar_empleado.html', datos)


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
            return redirect('/personal/empleados')
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
    return render(request, 'editar_empleado.html', datos)


def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    return redirect('/personal/empleados')