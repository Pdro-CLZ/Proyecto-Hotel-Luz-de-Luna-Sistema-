from django import forms
from .models import Inventario

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'descripcion', 'tipo', 'cantidad', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'input-text'}),
            'descripcion': forms.Textarea(attrs={'class':'textarea', 'rows':3}),
            'tipo': forms.Select(attrs={'class':'select-box'}),
            'cantidad': forms.NumberInput(attrs={'class':'input-text'}),
            'activo': forms.CheckboxInput(),
        }
