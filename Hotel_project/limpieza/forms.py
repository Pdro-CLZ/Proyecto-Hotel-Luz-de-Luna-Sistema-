from django import forms
from .models import ZonaLimpieza, TareaLimpieza

class ZonaLimpiezaForm(forms.ModelForm):
    detalles = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Detalles',
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )

    class Meta:
        model = ZonaLimpieza
        fields = ['nombre', 'detalles', 'foto', 'is_habitacion']
        labels = {
            'nombre': 'Nombre de la Zona',
            'detalles': 'Detalles',
            'foto': 'Foto de la Zona (opcional)',
            'is_habitacion': '¿Es una habitación?',
        }
        widgets = {
            'detalles': forms.Textarea(attrs={'rows': 3}),
            'foto': forms.FileInput,
        }
        error_messages = {
            'nombre': {
                'required': 'Este campo es obligatorio.',
                'max_length': 'Nombre muy extenso, máximo 25 caracteres.',
            },
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) > 25:
            raise forms.ValidationError("Nombre muy extenso, máximo 25 caracteres.")
        return nombre


class TareaLimpiezaForm(forms.ModelForm):
    detalles = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label='Detalles',
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )

    class Meta:
        model = TareaLimpieza
        fields = ['nombre', 'detalles', 'foto']
        labels = {
            'nombre': 'Nombre de la Tarea',
            'detalles': 'Detalles',
            'foto': 'Foto de la Tarea (opcional)',
        }
        widgets = {
            'detalles': forms.Textarea(attrs={'rows': 2}),
            'foto': forms.FileInput,
        }
        error_messages = {
            'nombre': {
                'required': 'Este campo es obligatorio.',
                'max_length': 'Nombre muy extenso, máximo 25 caracteres.',
            },
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) > 25:
            raise forms.ValidationError("Nombre muy extenso, máximo 25 caracteres.")
        return nombre
