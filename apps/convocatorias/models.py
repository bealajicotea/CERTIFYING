from django.db import models
from apps.usuarios.models import Usuario

# Create your models here.
class Convocatoria(models.Model):
    TIPO_CONVOCATORIA = [
        ('entrevista', 'Entrevista'),
        ('certificacion', 'Certificación'),
        ('curso', 'Curso'),
        ('colocacion', 'Colocación'),
        ('revalorizacion', 'Revalorización')
    ]
    niveles = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2')
    ]
    
    lugares = [
        ('Docente 1', 'Docente 1'),
        ('Docente 2', 'Docente 2'),
        ('Docente 3', 'Docente 3'),
        ('Docente 4', 'Docente 4'),
        ('Docente 5', 'Docente 5'),
        ('Docente 6', 'Docente 6')
        
    ]
    nivel = models.CharField(max_length=2, choices=niveles, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CONVOCATORIA)
    descripcion = models.TextField(max_length=300)
    lugar = models.CharField(max_length=100, choices=lugares)
    fecha = models.DateField(blank=True, null=True)  # Permitir nulos temporalmente
    hora = models.TimeField()
    profesor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'profesor'},
        null=True,  # <-- Permitir nulos temporalmente
        blank=True
    )  # Creador
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.fecha}"
