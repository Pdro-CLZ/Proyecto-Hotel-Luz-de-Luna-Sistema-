from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.utils import timezone

from .models import ZonaLimpieza, TareaLimpieza
from .forms import ZonaLimpiezaForm, TareaLimpiezaForm


@login_required
def registrar_zona(request):
    TareaFormSet = modelformset_factory(TareaLimpieza, form=TareaLimpiezaForm, extra=1, can_delete=True)

    if request.method == 'POST':
        zona_form = ZonaLimpiezaForm(request.POST, request.FILES)
        formset = TareaFormSet(request.POST, request.FILES, queryset=TareaLimpieza.objects.none())

        if zona_form.is_valid() and formset.is_valid():
            tareas_validas = [form for form in formset if form.cleaned_data.get('nombre') and form.cleaned_data.get('detalles')]
            if not tareas_validas:
                messages.error(request, "Debe registrar al menos una tarea con nombre y detalles.")
            else:
                zona = zona_form.save(commit=False)
                zona.usuario_registro = request.user
                zona.fecha_registro = timezone.now()
                zona.save()

                for form in tareas_validas:
                    tarea = form.save(commit=False)
                    tarea.zona = zona
                    tarea.usuario_modifica = request.user
                    tarea.save()

                messages.success(request, "Registro satisfactorio")
                return redirect('lista_zonas')
        else:
            messages.error(request, "Por favor revise los campos marcados.")
    else:
        zona_form = ZonaLimpiezaForm()
        formset = TareaFormSet(queryset=TareaLimpieza.objects.none())

    return render(request, 'limpieza/agregar_zona.html', {
        'zona_form': zona_form,
        'formset': formset
    })


@login_required
def index_limpieza(request):
    return render(request, 'limpieza/index_limpieza.html')


@login_required
def lista_zonas(request):
    zonas = ZonaLimpieza.objects.all().order_by('-fecha_registro')
    return render(request, 'limpieza/lista_zonas.html', {'zonas': zonas})


@login_required
def editar_zona(request, zona_id):
    zona = get_object_or_404(ZonaLimpieza, id=zona_id)
    TareaFormSet = modelformset_factory(TareaLimpieza, form=TareaLimpiezaForm, extra=0, can_delete=True, max_num=10)

    if request.method == 'POST':
        zona_form = ZonaLimpiezaForm(request.POST, request.FILES, instance=zona)
        formset = TareaFormSet(request.POST, request.FILES, queryset=zona.tareas.all())

        if zona_form.is_valid() and formset.is_valid():
            if 'eliminar_foto' in request.POST and zona.foto:
                zona.foto.delete()
                zona.foto = None

            zona_form.save()

            for i, form in enumerate(formset):
                tarea = form.save(commit=False)
                if tarea.pk is None:
                    tarea.zona = zona
                if f'eliminar_tarea_{i}' in request.POST and tarea.foto:
                    tarea.foto.delete()
                    tarea.foto = None
                tarea.usuario_modifica = request.user
                tarea.save()
                if form.cleaned_data.get('DELETE'):
                    tarea.delete()

            return redirect('lista_zonas')
    else:
        zona_form = ZonaLimpiezaForm(instance=zona)
        formset = TareaFormSet(queryset=zona.tareas.all())

    return render(request, 'limpieza/editar_zona.html', {
        'zona_form': zona_form,
        'formset': formset,
        'zona': zona
    })


@login_required
def lista_zonas_empleado(request):
    habitaciones = ZonaLimpieza.objects.filter(is_habitacion=True).order_by('nombre')
    otras_zonas = ZonaLimpieza.objects.filter(is_habitacion=False).order_by('nombre')
    return render(request, 'limpieza/lista_zonas_empleado.html', {
        'habitaciones': habitaciones,
        'otras_zonas': otras_zonas
    })


@login_required
def gestionar_zona(request, zona_id):
    zona = get_object_or_404(ZonaLimpieza, id=zona_id)
    tareas = TareaLimpieza.objects.filter(zona=zona)
    mensaje_alerta = None

    if request.method == "POST" and "cambiar_estado_zona" in request.POST:
        nuevo_estado = request.POST.get("nuevo_estado", "").strip()
        if nuevo_estado:
            tareas_pendientes = zona.tareas.filter(estado="Pendiente").count()
            if nuevo_estado == "Limpio (Disponible)" and tareas_pendientes > 0:
                mensaje_alerta = "No se puede cambiar a Limpio (Disponible) hasta que se completen todas las tareas."
            else:
                zona.estado = nuevo_estado
                zona.save()
                messages.success(request, f"Estado de la zona actualizado a {nuevo_estado}")
                return redirect("gestionar_zona", zona_id=zona.id)

    return render(request, 'limpieza/gestionar_zona.html', {
        'zona': zona,
        'tareas': tareas,
        'mensaje_alerta': mensaje_alerta
    })


@login_required
def cambiar_estado_tarea(request, tarea_id):
    tarea = get_object_or_404(TareaLimpieza, id=tarea_id)
    if request.method == "POST":
        nueva_observacion = request.POST.get("observaciones", "").strip()
        if tarea.estado == "Pendiente":
            tarea.estado = "Realizada"
        else:
            tarea.estado = "Pendiente"
        tarea.observaciones_empleado = nueva_observacion if nueva_observacion else tarea.observaciones_empleado
        tarea.save()
    return redirect("gestionar_zona", zona_id=tarea.zona.id)
