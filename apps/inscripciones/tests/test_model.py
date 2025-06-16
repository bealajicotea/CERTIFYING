from django.test import TestCase
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria
from apps.inscripciones.models import Inscripcion
from apps.resultados.models import Resultado

class InscripcionModelTest(TestCase):
    def setUp(self):
        self.estudiante = Usuario.objects.create_user(
            username='estudiante1',
            password='testpass123',
            tipo_usuario='estudiante'
        )
        self.profesor = Usuario.objects.create_user(
            username='profesor1',
            password='testpass123',
            tipo_usuario='profesor'
        )
        self.convocatoria = Convocatoria.objects.create(
            tipo='certificacion',
            descripcion='Convocatoria de prueba',
            lugar='Docente 1',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor
        )

    def test_crear_inscripcion(self):
        inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria
        )
        self.assertEqual(inscripcion.estudiante, self.estudiante)
        self.assertEqual(inscripcion.convocatoria, self.convocatoria)
        self.assertEqual(inscripcion.estado, 'pendiente')
        self.assertIsNotNone(inscripcion.fecha_inscripcion)
        self.assertIsNotNone(inscripcion.fecha_creacion)
        self.assertEqual(str(inscripcion), f"{self.estudiante.username} - {self.convocatoria}")

    def test_unique_constraint(self):
        Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria
        )
        with self.assertRaises(Exception):
            Inscripcion.objects.create(
                estudiante=self.estudiante,
                convocatoria=self.convocatoria
            )

    def test_resultado_property_none(self):
        inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria
        )
        self.assertIsNone(inscripcion.resultado)

    def test_estado_personalizado(self):
        inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria,
            estado='aprobado'
        )
        self.assertEqual(inscripcion.estado, 'aprobado')

    def test_resultado_property_with_resultado(self):
        inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria
        )
        resultado = Resultado.objects.create(
            inscripcion=inscripcion,
            nota='A2'
        )
        self.assertEqual(inscripcion.resultado, resultado)