from django import forms
from .models import Inscripcion


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'convocatoria']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control estudiante-field'}),
            'convocatoria': forms.Select(attrs={'class': 'form-control convocatoria-field'}),
        }
