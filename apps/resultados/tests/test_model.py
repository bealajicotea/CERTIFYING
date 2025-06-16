from django.test import TestCase
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria
from apps.inscripciones.models import Inscripcion
from apps.resultados.models import Resultado

class ResultadoModelTest(TestCase):
    def setUp(self):
        # Crear un profesor y un estudiante
        self.profesor = Usuario.objects.create_user(
            username='profesor1',
            password='testpass123',
            tipo_usuario='profesor'
        )
        self.estudiante = Usuario.objects.create_user(
            username='estudiante1',
            password='testpass123',
            tipo_usuario='estudiante'
        )
        # Crear una convocatoria
        self.convocatoria = Convocatoria.objects.create(
            tipo='certificacion',
            descripcion='Convocatoria de prueba',
            lugar='Docente 1',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor
        )
        # Crear una inscripción
        self.inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria
        )

    def test_crear_resultado(self):
        resultado = Resultado.objects.create(
            inscripcion=self.inscripcion,
            nota='A2',
            notaL='A2',
            notaE='A2',
            notaC='A2',
            notaO='A2'
        )
        self.assertEqual(resultado.nota, 'A2')
        self.assertEqual(resultado.inscripcion, self.inscripcion)
        self.assertEqual(str(resultado), f"{self.estudiante.username} - {self.convocatoria} - A2")

    def test_resultado_campos_opcionales(self):
        resultado = Resultado.objects.create(
            inscripcion=self.inscripcion
        )
        self.assertIsNone(resultado.nota)
        self.assertIsNone(resultado.notaL)
        self.assertIsNone(resultado.notaE)
        self.assertIsNone(resultado.notaC)
        self.assertIsNone(resultado.notaO)

    def test_resultado_fecha_creacion(self):
        resultado = Resultado.objects.create(
            inscripcion=self.inscripcion
        )
        self.assertIsNotNone(resultado.fecha_creacion)
        self.assertTrue(isinstance(resultado.fecha_creacion, timezone.datetime))

    def test_resultado_relacion_inscripcion(self):
        resultado = Resultado.objects.create(
            inscripcion=self.inscripcion,
            nota='B1'
        )
        self.assertEqual(resultado.inscripcion.estudiante.username, 'estudiante1')