from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Rol
import re

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'cedula', 'telefono', 'direccion', 'rol', 'password1', 'password2']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise ValidationError("Solo se permiten números")
        if len(telefono) != 8:
            raise ValidationError("Teléfono con cantidad de números indebida")
        return telefono

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Validar solo letras y espacios
        if not re.fullmatch(r"[A-Za-z ]+", username):
            raise ValidationError("Caracteres indebidos")
        return username

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        # Ejemplo simple de validación de cédula: 9 dígitos
        if not cedula.isdigit() or len(cedula) != 9:
            raise ValidationError("Formato de cédula inválido")
        # Verificar duplicado
        if Usuario.objects.filter(cedula=cedula).exists():
            raise ValidationError("Este usuario ya se encuentra registrado")
        return cedula

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya se encuentra registrado")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su usuario", "required": "true"})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña", "required": "true"})
    )

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "telefono", "email", "direccion", "cedula", "rol"]
        widgets = {
            "rol": forms.Select(),
        }

class ModificarMiUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "telefono", "email", "direccion", "cedula"]


class RolForm(forms.ModelForm):

    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', nombre):
            raise forms.ValidationError("Nombre con caracteres indebidos")
        return nombre