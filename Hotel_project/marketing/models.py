from django.db import models
from django.utils import timezone
import os
from ckeditor.fields import RichTextField

def upload_to(instance, filename):
    return os.path.join('plantillas', instance.nombre, filename)

class ContactoMarketing(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.correo}"
    

class PlantillaMarketing(models.Model):
    nombre = models.CharField(max_length=100)
    asunto = models.CharField(max_length=200)
    contenido_html = RichTextField()  # <-- esto reemplaza el textarea
    imagen = models.ImageField(upload_to='plantillas/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class CampaniaMarketing(models.Model):
    nombre = models.CharField(max_length=150)
    plantilla = models.ForeignKey(PlantillaMarketing, on_delete=models.CASCADE, null=True, blank=True)
    contactos = models.ManyToManyField(ContactoMarketing)
    fecha_envio = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=50, default="Pendiente")

    def __str__(self):
        return self.nombre
