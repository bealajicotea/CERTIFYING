from django import forms
from .models import Usuario, Convocatoria, Resultado, Inscripcion

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name',
            'tipo_usuario', 'facultad', 'grupo', 'anio_escolar',
            'carrera', 'curso', 'nivel', 'foto_perfil'  # <-- Agregado aquí
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control username-field'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control password-field'}),
            'email': forms.EmailInput(attrs={'class': 'form-control email-field'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control first-name-field'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control last-name-field'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control tipo-usuario-field'}),
            'facultad': forms.TextInput(attrs={'class': 'form-control facultad-field'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control grupo-field'}),
            'anio_escolar': forms.Select(attrs={'class': 'form-control anio-escolar-field'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control carrera-field'}),
            'curso': forms.TextInput(attrs={'class': 'form-control curso-field'}),
            'nivel': forms.TextInput(attrs={'class': 'form-control nivel-field'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control foto-perfil-field'}),  # <-- Agregado aquí
        }

class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = ['tipo', 'descripcion', 'lugar', 'fecha', 'hora', 'profesor', 'nivel', 'estado']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control tipo-field'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control descripcion-field'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control lugar-field'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-field', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control hora-field', 'type': 'time'}),
            'profesor': forms.Select(attrs={'class': 'form-control profesor-field'}),
            'nivel': forms.Select(attrs={'class': 'form-control nivel-field'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'convocatoria']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control estudiante-field'}),
            'convocatoria': forms.Select(attrs={'class': 'form-control convocatoria-field'}),
        }

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['nota', 'inscripcion']
        widgets = {
            'nota': forms.Select(attrs={'class': 'form-control nota-field'}),
            'inscripcion': forms.Select(attrs={'class': 'form-control inscripcion-field'}),
        }
