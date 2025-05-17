from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser): 
    TIPO_USUARIO = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor del Centro')
    ]

    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO)
    facultad = models.CharField(max_length=20)
    grupo = models.CharField(max_length=20,null=True, blank=True)
    anio_escolar = models.CharField(max_length=30,null=True, blank=True)
    carrera = models.CharField(max_length=100,null=True, blank=True)
    curso = models.CharField(max_length=30, blank=True, null=True)
    nivel = models.CharField(max_length=10,null=True, blank=True)
    def es_profesor(self):
        return self.tipo_usuario == 'profesor'

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"

class Convocatoria(models.Model):
    TIPO_CONVOCATORIA = [
        ('entrevista', 'Entrevista'),
        ('certificacion', 'Certificación')
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CONVOCATORIA)
    descripcion = models.TextField()
    lugar = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Creador

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.fecha}"

class Resultado(models.Model):
    TIPO_EXAMEN = [
        ('certificacion', 'Certificación'),
        ('entrevista', 'Entrevista'),
        ('curso', 'Curso')
    ]

    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'estudiante'})
    tipo_examen = models.CharField(max_length=20, choices=TIPO_EXAMEN)
    nivel = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.estudiante.username} - {self.tipo_examen} - {self.nivel}"

class Inscripcion(models.Model):
    TIPO_EXAMEN = [
        ('certificacion', 'Certificación'),
        ('entrevista', 'Entrevista'),
        ('curso', 'Curso')
    ]

    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'estudiante'})
    tipo_examen = models.CharField(max_length=20, choices=TIPO_EXAMEN)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.username} - {self.tipo_examen}"
