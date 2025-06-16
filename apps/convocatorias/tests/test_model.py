from django.test import TestCase
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria

class ConvocatoriaModelTest(TestCase):
    def setUp(self):
        self.profesor = Usuario.objects.create_user(
            username='profesor1',
            password='testpass123',
            tipo_usuario='profesor'
        )

    def test_crear_convocatoria(self):
        convocatoria = Convocatoria.objects.create(
            tipo='certificacion',
            descripcion='Convocatoria de prueba',
            lugar='Docente 1',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor,
            nivel='A2'
        )
        self.assertEqual(convocatoria.tipo, 'certificacion')
        self.assertEqual(convocatoria.profesor, self.profesor)
        self.assertEqual(convocatoria.lugar, 'Docente 1')
        self.assertEqual(convocatoria.nivel, 'A2')
        self.assertTrue(convocatoria.estado)
        self.assertEqual(str(convocatoria), f"Certificacion - {convocatoria.fecha}")

    def test_estado_default_activo(self):
        convocatoria = Convocatoria.objects.create(
            tipo='curso',
            descripcion='Curso de inglés',
            lugar='Docente 2',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor
        )
        self.assertTrue(convocatoria.estado)

    def test_fecha_creacion_auto(self):
        convocatoria = Convocatoria.objects.create(
            tipo='entrevista',
            descripcion='Entrevista de prueba',
            lugar='Docente 3',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor
        )
        self.assertIsNotNone(convocatoria.fecha_creacion)

    def test_profesor_puede_ser_nulo(self):
        convocatoria = Convocatoria.objects.create(
            tipo='colocacion',
            descripcion='Colocación sin profesor',
            lugar='Docente 4',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=None
        )
        self.assertIsNone(convocatoria.profesor)

    def test_nivel_opcional(self):
        convocatoria = Convocatoria.objects.create(
            tipo='revalorizacion',
            descripcion='Revalorización sin nivel',
            lugar='Docente 5',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor,
            nivel=None
        )
        self.assertIsNone(convocatoria.nivel)