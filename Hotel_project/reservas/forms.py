from django import forms
from .models import Habitacion


class PrecioRangoForm(forms.Form):
    habitacion = forms.ModelChoiceField(
        queryset=Habitacion.objects.all(),
        label="Habitación"
    )
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    precio = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio por noche")
