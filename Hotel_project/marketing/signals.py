from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import PlantillaMarketing

@receiver(post_migrate)
def crear_plantillas_default(sender, **kwargs):
    if sender.name == 'marketing':
        if PlantillaMarketing.objects.count() == 0:
            PlantillaMarketing.objects.create(
                nombre="Bienvenida",
                asunto="¡Bienvenido a Hotel Luz de Luna!",
                contenido_html="<h1>Bienvenido</h1><p>Gracias por preferirnos. Esperamos verte pronto.</p>"
            )
            PlantillaMarketing.objects.create(
                nombre="Oferta Especial",
                asunto="¡Disfruta de nuestras ofertas especiales!",
                contenido_html="<h2>Promoción del mes</h2><p>Descuento del 20% para estancias de más de 3 noches.</p>"
            )
