from django import forms
from django.contrib.auth.forms import UserCreationForm
from administracion.models import Usuario, Rol
from personal.models import Direccion
from sitio_web.models import Cliente   

class RegistroClienteForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True, label="Nombre")
    apellido = forms.CharField(max_length=50, required=True, label="Apellidos")
    cedula = forms.CharField(max_length=9, required=True, label="Cédula")
    email = forms.EmailField(label="Correo electrónico")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    # Dirección
    direccion_exacta = forms.CharField(max_length=100, required=True, label="Dirección exacta")
    pais = forms.CharField(max_length=50, required=True, label="País")
    provincia = forms.CharField(max_length=50, required=True, label="Provincia")
    canton = forms.CharField(max_length=50, required=True, label="Cantón")
    distrito = forms.CharField(max_length=50, required=True, label="Distrito")

    # Contacto
    telefono = forms.CharField(max_length=15, required=True, label="Teléfono")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Correo registrado")
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        if Usuario.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError("Esta cédula ya está registrada.")
        return cedula

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

class EditarPerfilForm(forms.Form):
    # Datos personales
    nombre = forms.CharField(max_length=50, label="Nombre")
    apellido = forms.CharField(max_length=50, label="Apellido")
    email = forms.EmailField(label="Correo electrónico")

    # Teléfono
    telefono = forms.CharField(max_length=15, label="Teléfono")

    # Dirección
    direccion_exacta = forms.CharField(max_length=100, label="Dirección exacta")
    pais = forms.CharField(max_length=50, label="País")
    provincia = forms.CharField(max_length=50, label="Provincia")
    canton = forms.CharField(max_length=50, label="Cantón")
    distrito = forms.CharField(max_length=50, label="Distrito")

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if self.usuario:
            # Inicializar campos con datos actuales
            self.fields['nombre'].initial = self.usuario.first_name
            self.fields['apellido'].initial = self.usuario.last_name
            self.fields['email'].initial = self.usuario.email
            self.fields['telefono'].initial = self.usuario.cliente.telefono
            direccion = self.usuario.cliente.direccion
            self.fields['direccion_exacta'].initial = direccion.direccion_exacta
            self.fields['pais'].initial = direccion.pais.nombre
            self.fields['provincia'].initial = direccion.provincia.nombre
            self.fields['canton'].initial = direccion.canton.nombre
            self.fields['distrito'].initial = direccion.distrito.nombre
            
from django import forms
from datetime import date

class ConsultaDisponibilidadForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today_str = date.today().isoformat()
        self.fields['fecha_inicio'].widget.attrs['min'] = today_str
        self.fields['fecha_fin'].widget.attrs['min'] = today_str

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        hoy = date.today()

        if fecha_inicio and fecha_inicio < hoy:
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser anterior a hoy.')

        if fecha_fin and fecha_fin < hoy:
            self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a hoy.')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_fin', 'La fecha de fin debe ser posterior a la de inicio.')

        return cleaned_data

