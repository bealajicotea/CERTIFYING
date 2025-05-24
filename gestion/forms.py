from django import forms
from .models import Usuario, Convocatoria, Resultado, Inscripcion

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name',
            'tipo_usuario', 'facultad', 'anio_escolar', 'grupo',
            'carrera', 'curso', 'nivel', 'foto_perfil'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control username-field', 'id': 'id-username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control password-field', 'id': 'id-password'}),
            'email': forms.EmailInput(attrs={'class': 'form-control email-field', 'id': 'id-email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control first-name-field', 'id': 'id-first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control last-name-field', 'id': 'id-last_name'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control tipo-usuario-field', 'id': 'id-tipo_usuario'}),
            'facultad': forms.Select(attrs={'class': 'form-control', 'id': 'id-facultad'}),
            'anio_escolar': forms.Select(attrs={'class': 'form-control', 'id': 'id-anio_escolar'}),
            'grupo': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'id-grupo'}),
            'carrera': forms.Select(attrs={'class': 'form-control carrera-field', 'id': 'id-carrera'}),
            'curso': forms.TextInput(attrs={'class': 'form-control curso-field', 'id': 'id-curso'}),
            'nivel': forms.Select(attrs={'class': 'form-control nivel-field', 'id': 'id-nivel'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control foto-perfil-field', 'id': 'id-foto_perfil'}),
        }

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
