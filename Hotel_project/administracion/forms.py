from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Rol
from personal.models import Empleado, Direccion, Pais, Provincia, Canton, Distrito
import re
from django.contrib.auth.password_validation import validate_password


# ---------------- Registro de Usuario ----------------
class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'cedula', 'rol', 'password1', 'password2']
        labels = {
            'username': 'Usuario',
            'email': 'Correo electrónico',
            'cedula': 'Cédula',
            'rol': 'Rol',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.fullmatch(r"[A-Za-z ]+", username):
            raise ValidationError("Caracteres indebidos")
        return username

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit() or len(cedula) != 9:
            raise ValidationError("Formato de cédula inválido")
        if Usuario.objects.filter(cedula=cedula).exists():
            raise ValidationError("Este usuario ya se encuentra registrado")
        return cedula

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya se encuentra registrado")
        return email

# ---------------- Login ----------------
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su usuario", "required": "true"})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña", "required": "true"})
    )

# ---------------- Editar Usuario (Administrador) ----------------
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username", "email", "cedula", "rol"]
        labels = {
            'username': 'Usuario',
            'email': 'Correo electrónico',
            'cedula': 'Cédula',
            'rol': 'Rol',
        }
        widgets = {
            "rol": forms.Select(),
        }
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.fullmatch(r"[A-Za-z ]+", username):
            raise ValidationError("Caracteres indebidos")
        return username

# ---------------- Modificar Mi Usuario ----------------
class ModificarMiUsuarioForm(forms.ModelForm):

    nombre = forms.CharField(required=False, label="Nombre")
    apellido = forms.CharField(required=False, label="Apellido")
    telefono = forms.CharField(required=False, label="Teléfono")
    
    direccion_exacta = forms.CharField(required=False, label="Dirección exacta")
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), required=False)
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(), required=False)
    canton = forms.ModelChoiceField(queryset=Canton.objects.all(), required=False)
    distrito = forms.ModelChoiceField(queryset=Distrito.objects.all(), required=False)

    class Meta:
        model = Usuario
        fields = ["username", "cedula", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self.instance, 'empleado'):
            empleado = self.instance.empleado
            self.fields['nombre'].initial = empleado.nombre
            self.fields['apellido'].initial = empleado.apellido
            self.fields['telefono'].initial = empleado.telefono
            if empleado.direccion:
                self.fields['direccion_exacta'].initial = empleado.direccion.direccion_exacta
                self.fields['pais'].initial = empleado.direccion.pais
                self.fields['provincia'].initial = empleado.direccion.provincia
                self.fields['canton'].initial = empleado.direccion.canton
                self.fields['distrito'].initial = empleado.direccion.distrito

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if commit:
            usuario.save()
            if hasattr(usuario, 'empleado'):
                empleado = usuario.empleado
                empleado.nombre = self.cleaned_data.get('nombre')
                empleado.apellido = self.cleaned_data.get('apellido')
                empleado.telefono = self.cleaned_data.get('telefono')

                if empleado.direccion:
                    direccion = empleado.direccion
                    direccion.direccion_exacta = self.cleaned_data.get('direccion_exacta')
                    direccion.pais = self.cleaned_data.get('pais')
                    direccion.provincia = self.cleaned_data.get('provincia')
                    direccion.canton = self.cleaned_data.get('canton')
                    direccion.distrito = self.cleaned_data.get('distrito')
                    direccion.save()
                else:
                    nueva_direccion = Direccion.objects.create(
                        direccion_exacta=self.cleaned_data.get('direccion_exacta'),
                        pais=self.cleaned_data.get('pais'),
                        provincia=self.cleaned_data.get('provincia'),
                        canton=self.cleaned_data.get('canton'),
                        distrito=self.cleaned_data.get('distrito')
                    )
                    empleado.direccion = nueva_direccion

                empleado.save()
        return usuario

# ---------------- Rol ----------------
class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', nombre):
            raise forms.ValidationError("Nombre con caracteres indebidos")
        return nombre
