from django import forms
from .models import Empleado
from django.forms import DateInput
import re

class EmpleadoForm(forms.ModelForm):

    fecha_contratacion = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = Empleado
        fields = [
            'rol', 'nombre', 'apellido', 'cedula', 'telefono', 'correo',
            'fecha_contratacion', 'salario'
        ]

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', nombre):
            raise forms.ValidationError("Nombre con caracteres indebidos")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', apellido):
            raise forms.ValidationError("Apellido con caracteres indebidos")
        return apellido

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("Solo se permiten números")
        if len(telefono) < 8 or len(telefono) > 10:
            raise forms.ValidationError("Teléfono con cantidad de números indebida")
        return telefono

    def clean_salario(self):
        salario = self.cleaned_data.get('salario')
        if salario < 0:
            raise forms.ValidationError("Salario no puede ser negativo")
        return salario

    def clean_fecha_contratacion(self):
        fecha = self.cleaned_data.get('fecha_contratacion')
        if fecha is None:
            raise forms.ValidationError("Ingrese una fecha válida")
        return fecha
