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

    group = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'), ]

    cur = [
        ('Below A1','Below A1'),
        ('A1','A1'),
        ('A2','A2'),
        ('B1','B1'),
        ('B2','B2'),
        ('C1','C1'),
        ('C2','C2'),
    ]

    facultad = models.CharField(max_length=2, choices=fac, null=True, blank=True)
    anio_escolar = models.CharField(max_length=1, choices=anios, null=True, blank=True)
    grupo = models.CharField(max_length=20,choices= group, blank=True)
    carrera = models.CharField(max_length=100,choices=car, null=True, blank=True)
    curso = models.CharField(max_length=30, choices=cur, blank=True, null=True)
    nivel = models.CharField(max_length=10,choices= niveles,null=True, blank=True)
    foto_perfil = models.ImageField(upload_to=ruta_foto_perfil, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO)

    def es_profesor(self):
        return self.tipo_usuario == 'profesor'

    def es_estudiante(self):
        return self.tipo_usuario == 'estudiante'

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"

