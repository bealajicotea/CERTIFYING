from django.db import models
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria
from apps.resultados.models import Resultado

# Create your models here.
class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'estudiante'}
    )
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')  # ejemplo
    
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
