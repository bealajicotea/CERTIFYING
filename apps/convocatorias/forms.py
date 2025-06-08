from django import forms
from .models import Convocatoria

class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = ['tipo', 'descripcion', 'lugar', 'fecha', 'hora', 'profesor', 'nivel', 'estado']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control tipo-field'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control descripcion-field'}),
            'lugar': forms.Select(attrs={'class': 'form-control lugar-field'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-field', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control hora-field', 'type': 'time'}),
            'profesor': forms.Select(attrs={'class': 'form-control profesor-field'}),
            'nivel': forms.Select(attrs={'class': 'form-control nivel-field'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
