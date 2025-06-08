from django import forms
from .models import Resultado

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['nota', 'inscripcion']
        widgets = {
            'nota': forms.Select(attrs={'class': 'form-control nota-field'}),
            'inscripcion': forms.Select(attrs={'class': 'form-control inscripcion-field'}),
        }
