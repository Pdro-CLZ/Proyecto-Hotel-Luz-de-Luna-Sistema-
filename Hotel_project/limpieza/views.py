from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from .models import Limpieza, Habitacion,Zona, TareaLimpieza,TareaZona
from django.contrib import messages
from .forms import LimpiezaForm
from django.forms import modelformset_factory
from .forms import ZonaForm, TareaForm
from django.http import JsonResponse

# @login_required
def visualizar_estados(request):
    try:
        limpiezas = Limpieza.objects.all()
        zonas = Zona.objects.all()

        if not limpiezas and not zonas:
            return render(request, "limpieza/visualizar_estados.html", {
                "mensaje": "No hay estados de limpieza ni zonas registradas."
            })

        return render(request, "limpieza/visualizar_estados.html", {
            "limpiezas": limpiezas,
            "zonas": zonas
        })
    except Exception:
        return render(request, "limpieza/visualizar_estados.html", {
            "error": "No se ha podido cargar la página, consulte con el administrador o revise su conexión."
        })

    
def registrar_estado(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)

    if request.method == "POST":
        form = LimpiezaForm(request.POST)
        if form.is_valid():
            limpieza = form.save(commit=False)
            limpieza.habitacion = habitacion
            limpieza.empleado = request.user.empleado 
            limpieza.save()
            form.save_m2m()  
            messages.success(request, "Información registrada satisfactoriamente")
            return redirect("limpieza:visualizar_estados")
        else:
            messages.error(request, "Por favor seleccione una tarea por lo menos")
    else:
        form = LimpiezaForm()

    return render(request, "limpieza/registrar_estado.html", {
        "habitacion": habitacion,
        "form": form,
    })


def visualizar_estado(request, habitacion_id):
    try:
        habitacion = get_object_or_404(Habitacion, id=habitacion_id)
        limpieza = Limpieza.objects.filter(habitacion=habitacion).last()

        if not limpieza:
            messages.warning(request, "No hay registros de limpieza para esta habitación/zona.")
            return render(request, "limpieza/visualizar_estado.html", {"habitacion": habitacion})

        return render(request, "limpieza/visualizar_estado.html", {
            "habitacion": habitacion,
            "limpieza": limpieza,
            "tareas": limpieza.tareas.all() if hasattr(limpieza, "tareas") else [],
        })

    except Exception:
        return render(request, "limpieza/visualizar_estado.html", {
            "error": "No se ha podido cargar la página, consulte con el administrador o revise su conexión."
        })

def registrar_zona(request):
    TareaFormSet = modelformset_factory(TareaLimpieza, form=TareaForm, extra=1, can_delete=True)

    if request.method == "POST":
        zona_form = ZonaForm(request.POST, request.FILES)
        tarea_formset = TareaFormSet(request.POST, request.FILES, queryset=TareaLimpieza.objects.none())

        if zona_form.is_valid() and tarea_formset.is_valid():
            zona = zona_form.save()

            for form in tarea_formset:
                if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                    tarea = form.save(commit=False)
                    tarea.zona = zona
                    tarea.save()

            messages.success(request, "Registro satisfactorio")
            return redirect("limpieza:visualizar_estados")
        else:
            messages.error(request, "Revise los errores en el formulario")

    else:
        zona_form = ZonaForm()
        tarea_formset = TareaFormSet(queryset=TareaLimpieza.objects.none())

    return render(request, "limpieza/registrar_zona.html", {
        "zona_form": zona_form,
        "tarea_formset": tarea_formset,
    })

def actualizar_zona(request, zona_id):
    zona = get_object_or_404(Zona, id=zona_id)
    TareaFormSet = modelformset_factory(TareaZona, form=TareaForm, extra=0, can_delete=True)

    if request.method == "POST":
        zona_form = ZonaForm(request.POST, request.FILES, instance=zona)
        tarea_formset = TareaFormSet(request.POST, request.FILES, queryset=zona.tareas.all())

        if zona_form.is_valid() and tarea_formset.is_valid():
            zona_form.save()

            for form in tarea_formset:
                if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                    tarea = form.save(commit=False)
                    tarea.zona = zona
                    tarea.save()

            messages.success(request, "Actualización satisfactoria")
            return redirect("limpieza:visualizar_estados")
        else:
            messages.error(request, "Revise los errores en el formulario")

    else:
        zona_form = ZonaForm(instance=zona)
        tarea_formset = TareaFormSet(queryset=zona.tareas.all())

    return render(request, "limpieza/actualizar_zona.html", {
        "zona": zona,
        "zona_form": zona_form,
        "tarea_formset": tarea_formset,
    })

def buscar_zona(request):
    query = request.GET.get("q", "")
    resultados = []

    if query.isdigit():
        zonas = Zona.objects.filter(id=query)
    else:
        zonas = Zona.objects.filter(nombre__icontains=query)

    for zona in zonas:
        resultados.append({"id": zona.id, "nombre": zona.nombre})

    return JsonResponse({"resultados": resultados})
