from django import forms
from .models import Empleado
from administracion.models import Rol
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
        if len(telefono) != 8:
            raise forms.ValidationError("Teléfono con cantidad de números indebida")
        return telefono

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit() or len(cedula) != 9:
            raise forms.ValidationError("Formato de cédula inválido")
        empleadoQs = Empleado.objects.filter(cedula=cedula)
        if self.instance and self.instance.pk:
            empleadoQs = empleadoQs.exclude(pk=self.instance.pk)
        if empleadoQs.exists():
            raise forms.ValidationError("Este usuario ya se encuentra registrado")
        return cedula


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


class EmpleadoSeleccionForm(forms.Form):
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        empty_label="Seleccione un ID",
        label="Empleado",
        to_field_name="id"
    )

class FiltroAsistenciaForm(forms.Form):
    fecha = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        rol = cleaned_data.get("rol")

        if not rol:
            self.add_error("rol", "Debe seleccionar un rol.")
        if fecha and not rol:
            self.add_error("rol", "Debe seleccionar un rol para filtrar por fecha.")

        return cleaned_data
