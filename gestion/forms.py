from django import forms
from .models import Usuario, Convocatoria, Resultado, Inscripcion

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name',
            'tipo_usuario', 'facultad', 'grupo', 'anio_escolar',
            'carrera', 'curso', 'nivel'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = ['tipo', 'descripcion', 'lugar', 'fecha', 'hora', 'usuario']

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['estudiante', 'tipo_examen', 'nivel']

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'tipo_examen']
