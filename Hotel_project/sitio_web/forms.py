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