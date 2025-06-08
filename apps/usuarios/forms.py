from django import forms
from .models import Usuario

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
            'curso': forms.Select(attrs={'class': 'form-control curso-field', 'id': 'id-curso'}),
            'nivel': forms.Select(attrs={'class': 'form-control nivel-field', 'id': 'id-nivel'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control foto-perfil-field', 'id': 'id-foto_perfil'}),
        }