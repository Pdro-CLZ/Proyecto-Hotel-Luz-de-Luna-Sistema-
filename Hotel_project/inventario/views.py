from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Inventario
from .forms import InventarioForm

# --- Dashboard / listado ---
@login_required
def lista_inventario(request):
    tipo_filter = request.GET.get('tipo', '')
    estado_filter = request.GET.get('estado', '')

    items = Inventario.objects.all()

    if tipo_filter in ['Activo', 'Insumo']:
        items = items.filter(tipo=tipo_filter)
    if estado_filter == 'Activo':
        items = items.filter(activo=True)
    elif estado_filter == 'Inactivo':
        items = items.filter(activo=False)

    return render(request, 'inventario/lista_inventario.html', {
        'inventario': items,
        'tipo_filter': tipo_filter,
        'estado_filter': estado_filter,
    })


# --- Crear ---
@login_required
def crear_inventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item creado correctamente.")
            return redirect('lista_inventario')
    else:
        form = InventarioForm()
    return render(request, 'inventario/crear_inventario.html', {'form': form})


# --- Verificación de roles ---
def es_admin_o_manager(user):
    return user.rol and user.rol.nombre in ["Administrador", "Manager"]


# --- Editar completo (solo Admin/Manager) ---
@login_required
@user_passes_test(es_admin_o_manager)
def editar_inventario(request, pk):
    item = get_object_or_404(Inventario, pk=pk)
    if request.method == "POST":
        form = InventarioForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item actualizado correctamente.")
            return redirect("lista_inventario")
    else:
        form = InventarioForm(instance=item)

    return render(request, "inventario/editar_inventario.html", {"form": form, "item": item})


# --- Editar solo cantidad (para otros usuarios) ---
@login_required
def editar_cantidad_inventario(request, pk):
    item = get_object_or_404(Inventario, pk=pk)
    if request.method == "POST":
        cantidad = request.POST.get("cantidad")
        if cantidad and cantidad.isdigit():
            item.cantidad = int(cantidad)
            item.save()
            messages.success(request, "Cantidad actualizada correctamente.")
            return redirect("lista_inventario")
        else:
            messages.error(request, "Cantidad inválida.")

    return render(request, "inventario/editar_cantidad.html", {"item": item})


# --- Activar / Inactivar ---
@login_required
@user_passes_test(es_admin_o_manager)
def activar_inactivar_inventario(request, pk):
    item = get_object_or_404(Inventario, pk=pk)
    item.activo = not item.activo
    item.save()
    estado = "activado" if item.activo else "inactivado"
    messages.success(request, f"Item {estado}.")
    return redirect('lista_inventario')
