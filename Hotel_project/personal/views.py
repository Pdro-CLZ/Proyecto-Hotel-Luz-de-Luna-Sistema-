from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import time, datetime, timedelta
from .models import Empleado, Asistencia

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

    return render(request, "index.html", {
        "empleado": empleado,
        "mensaje": mensaje,
        "hora_marca_ingreso": hora_marca_ingreso,
        "hora_marca_salida": hora_marca_salida,
    })
