from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PlantillaMarketing, ContactoMarketing, CampaniaMarketing
import threading
from django.core.mail import EmailMessage

def dashboard_marketing(request):
    return render(request, 'marketing/dashboard.html')

# --- Plantillas ---
def lista_plantillas(request):
    plantillas = PlantillaMarketing.objects.all()
    return render(request, 'marketing/lista_plantillas.html', {'plantillas': plantillas})

def crear_plantilla(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        asunto = request.POST.get('asunto')
        contenido_html = request.POST.get('contenido_html')
        imagen = request.FILES.get('imagen')
        PlantillaMarketing.objects.create(
            nombre=nombre, asunto=asunto, contenido_html=contenido_html, imagen=imagen
        )
        messages.success(request, "Plantilla creada correctamente.")
        return redirect('lista_plantillas')
    return render(request, 'marketing/crear_plantilla.html')

def editar_plantilla(request, pk):
    plantilla = get_object_or_404(PlantillaMarketing, pk=pk)
    if request.method == 'POST':
        plantilla.nombre = request.POST.get('nombre')
        plantilla.asunto = request.POST.get('asunto')
        plantilla.contenido_html = request.POST.get('contenido_html')
        if request.FILES.get('imagen'):
            plantilla.imagen = request.FILES['imagen']
        plantilla.save()
        messages.success(request, "Plantilla actualizada.")
        return redirect('lista_plantillas')
    return render(request, 'marketing/editar_plantilla.html', {'plantilla': plantilla})

def eliminar_plantilla(request, pk):
    plantilla = get_object_or_404(PlantillaMarketing, pk=pk)
    plantilla.delete()
    messages.success(request, "Plantilla eliminada correctamente.")
    return redirect('lista_plantillas')

def crear_campania(request):
    plantillas = PlantillaMarketing.objects.all()
    contactos = ContactoMarketing.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        plantilla_id = request.POST.get('plantilla')
        plantilla = get_object_or_404(PlantillaMarketing, pk=plantilla_id)
        
        # Crear la campaña en la base de datos
        campania = CampaniaMarketing.objects.create(nombre=nombre, plantilla=plantilla)
        campania.contactos.set(contactos)
        campania.save()
        
        # Enviar correos en segundo plano
        thread = threading.Thread(target=enviar_emails, args=(contactos, plantilla))
        thread.start()
        
        messages.success(request, "Campaña creada. Los correos se están enviando en segundo plano.")
        return redirect('dashboard_marketing')
    
    return render(request, 'marketing/crear_campania.html', {'plantillas': plantillas})


def enviar_emails(contactos, plantilla):
    for contacto in contactos:
        email = EmailMessage(
            subject=plantilla.asunto,
            body=plantilla.contenido_html,
            from_email=None,  # usa DEFAULT_FROM_EMAIL
            to=[contacto.correo],
        )
        email.content_subtype = "html"

        # Adjuntar imagen si existe
        if plantilla.imagen:
            email.attach_file(plantilla.imagen.path)

        email.send(fail_silently=True)

