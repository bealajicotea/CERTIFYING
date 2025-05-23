from django.contrib.auth.models import AbstractUser
from django.db import models

def ruta_foto_perfil(instance, filename):
    return f'fotos_perfil/user_{instance.id}/{filename}'



class Usuario(AbstractUser): 
    TIPO_USUARIO = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor del Centro'),
    ]
    anios =[
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),
        ('4', 'Cuarto'),
    ]

    car =[  
        ('1','Ingenieria en Ciencias Informáticas'),
        ('2','Ciberseguridad'),
        ('3', 'Bioinformática'),
        ('4', 'Redes y Seguridad Informática'),
    ]

    niveles = [
        ('A1','A1'),
        ('A2','A2'),
        ('B1','B1'),
        ('B2','B2'),
        ('C1','C1'),
        ('C2','C2'),
    ]

    fac = [
        ('1','FTL'),
        ('2','FCS'),
        ('3','FIO'),
        ('4','FTI'),
        ('5','CITEC'),
        ('6','FTE'),
    ]
    facultad = models.CharField(max_length=2, choices=fac, null=True, blank=True)
    anio_escolar = models.CharField(max_length=1, choices=anios, null=True, blank=True)
    grupo = models.CharField(max_length=20, blank=True)
    carrera = models.CharField(max_length=100,choices=car, null=True, blank=True)
    curso = models.CharField(max_length=30, blank=True, null=True)
    nivel = models.CharField(max_length=10,choices= niveles,null=True, blank=True)
    foto_perfil = models.ImageField(upload_to=ruta_foto_perfil, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO)

    def es_profesor(self):
        return self.tipo_usuario == 'profesor'

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"

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
    fecha = models.DateField()
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

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'estudiante'}
    )
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['estudiante', 'convocatoria'], name='unique_inscripcion_estudiante_convocatoria')
        ]

    def __str__(self):
        return f"{self.estudiante.username} - {self.convocatoria}"

    @property
    def resultado(self):
        try:
            return self.resultado_set.get()
        except Resultado.DoesNotExist:
            return None

class Resultado(models.Model):
    niveles = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2')
    ]
    nota = models.CharField(max_length=2, choices=niveles)
    inscripcion = models.OneToOneField('Inscripcion', on_delete=models.CASCADE)
    # Otros campos que necesites

    def __str__(self):
        return f"{self.inscripcion.estudiante.username} - {self.inscripcion.convocatoria} - {self.nota}"
