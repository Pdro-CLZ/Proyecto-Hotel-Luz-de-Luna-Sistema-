from django import forms
from .models import Limpieza, TareaLimpieza , Zona


class LimpiezaForm(forms.ModelForm):
    tareas = forms.ModelMultipleChoiceField(
        queryset=TareaLimpieza.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Limpieza
        fields = ["estado", "observaciones", "tareas"]

    def clean_tareas(self):
        tareas = self.cleaned_data.get("tareas")
        if not tareas:
            raise forms.ValidationError("Por favor seleccione una tarea por lo menos")
        return tareas



class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ["nombre", "foto"]
        labels = {
            "nombre": "Nombre de la zona",
            "foto": "Foto de la zona"
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = TareaLimpieza
        fields = ["nombre", "icono"]   # 👈 corregido
        labels = {
            "nombre": "Nombre de la tarea",
            "icono": "Icono / Foto de la tarea"
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if len(nombre) > 25:
            raise forms.ValidationError("nombre muy extenso")
        return nombre
