from django.utils import timezone
from django.db import models

class Resultado(models.Model):

    NIVELES = [
        ('BELLOW A1', 'BELLOW A1'),
        ('A1', 'A1'),
        ('A1+', 'A1+'),
        ('A2', 'A2'),
        ('A2+', 'A2+'),
        ('B1', 'B1'),
        ('B1+', 'B1+'),
        ('B2', 'B2'),
        ('B2+', 'B2+'),
        ('C1', 'C1'),
        ('C1+', 'C1+'),
        ('C2', 'C2'),
    ]
    nota = models.CharField(max_length=10, choices=NIVELES, blank=True,null=True)
    notaL = models.CharField(max_length=10, choices=NIVELES, blank=True,null=True)
    notaE = models.CharField(max_length=10, choices=NIVELES, blank=True,null=True)
    notaC = models.CharField(max_length=10, choices=NIVELES, blank=True,null=True)
    notaO = models.CharField(max_length=10, choices=NIVELES, blank=True,null=True)
    fecha_creacion = models.DateTimeField(null=True, blank=True, default=timezone.now)


    inscripcion = models.ForeignKey('inscripciones.Inscripcion', on_delete=models.CASCADE)
    # Otros campos que necesites

    def __str__(self):
        return f"{self.inscripcion.estudiante.username} - {self.inscripcion.convocatoria} - {self.nota}"

