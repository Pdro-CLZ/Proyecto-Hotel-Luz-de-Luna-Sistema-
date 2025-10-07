from django import forms
from .models import Empleado, Direccion
from django.forms import DateInput
from administracion.models import Usuario
from django.db.models import Q
import re

class EmpleadoForm(forms.ModelForm):
    fecha_contratacion = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = Empleado
        fields = [
            'usuario', 'nombre', 'apellido', 'telefono', 'fecha_contratacion', 'salario'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            usuarios_disponibles = Usuario.objects.filter(
                Q(empleado__isnull=True) | Q(id=self.instance.usuario.id)
            )
        else:
            usuarios_disponibles = Usuario.objects.filter(empleado__isnull=True)

        self.fields['usuario'].queryset = usuarios_disponibles
        self.fields['usuario'].required = True 

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
    # Para filtrar por rol del usuario asociado al empleado
    rol_nombre = forms.CharField(required=False, label="Nombre del rol")

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        rol_nombre = cleaned_data.get("rol_nombre")

        if fecha and not rol_nombre:
            self.add_error("rol_nombre", "Debe seleccionar un rol para filtrar por fecha.")

        return cleaned_data
