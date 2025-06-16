from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria
from apps.inscripciones.models import Inscripcion
from apps.resultados.models import Resultado

class InscripcionesResultadosViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.convocatoria_cert = Convocatoria.objects.create(
            tipo='certificacion',
            descripcion='Certificación',
            lugar='Docente 1',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor,
            nivel='A2'
        )
        self.convocatoria_curso = Convocatoria.objects.create(
            tipo='curso',
            descripcion='Curso',
            lugar='Docente 2',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor,
            nivel='A1'
        )
        self.inscripcion_cert = Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria_cert
        )
        self.inscripcion_curso = Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria_curso
        )

    def test_evaluarInscripcion_requires_login(self):
        data = {'elemento_id': self.inscripcion_curso.id, 'codigo': 'A2'}
        response = self.client.post(reverse('evaluar_inscripcion'), data)
        self.assertRedirects(response, reverse('login'))

    def test_evaluarInscripcion_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        data = {'elemento_id': self.inscripcion_curso.id, 'codigo': 'A2'}
        response = self.client.post(reverse('evaluar_inscripcion'), data)
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_evaluarInscripcion_post_crea_resultado(self):
        self.client.login(username='profesor1', password='testpass123')
        data = {'elemento_id': self.inscripcion_curso.id, 'codigo': 'A2'}
        response = self.client.post(reverse('evaluar_inscripcion'), data)
        self.assertRedirects(response, reverse('lista_inscripciones'))
        resultado = Resultado.objects.get(inscripcion=self.inscripcion_curso)
        self.assertEqual(resultado.nota, 'A2')

    def test_evaluarInscripcion_post_actualiza_resultado(self):
        Resultado.objects.create(inscripcion=self.inscripcion_curso, nota='A1')
        self.client.login(username='profesor1', password='testpass123')
        data = {'elemento_id': self.inscripcion_curso.id, 'codigo': 'B1'}
        response = self.client.post(reverse('evaluar_inscripcion'), data)
        self.assertRedirects(response, reverse('lista_inscripciones'))
        resultado = Resultado.objects.get(inscripcion=self.inscripcion_curso)
        self.assertEqual(resultado.nota, 'B1')

    def test_evaluarInscripcion_actualiza_nivel_usuario_si_curso(self):
        self.client.login(username='profesor1', password='testpass123')
        data = {'elemento_id': self.inscripcion_curso.id, 'codigo': 'B2'}
        self.client.post(reverse('evaluar_inscripcion'), data)
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.nivel, 'B2')

    def test_evaluar_certificacion_requires_login(self):
        data = {
            'inscripcion_id': self.inscripcion_cert.id,
            'nota_oral': 'A2',
            'nota_comprension': 'A2',
            'nota_escritura': 'A2',
            'nota_audicion': 'A2'
        }
        response = self.client.post(reverse('evaluar_certificacion'), data)
        self.assertRedirects(response, reverse('login'))

    def test_evaluar_certificacion_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        data = {
            'inscripcion_id': self.inscripcion_cert.id,
            'nota_oral': 'A2',
            'nota_comprension': 'A2',
            'nota_escritura': 'A2',
            'nota_audicion': 'A2'
        }
        response = self.client.post(reverse('evaluar_certificacion'), data)
        self.assertRedirects(response, reverse('login'))

    def test_evaluar_certificacion_post(self):
        self.client.login(username='profesor1', password='testpass123')
        data = {
            'inscripcion_id': self.inscripcion_cert.id,
            'nota_oral': 'A2',
            'nota_comprension': 'A2',
            'nota_escritura': 'A2',
            'nota_audicion': 'A2'
        }
        response = self.client.post(reverse('evaluar_certificacion'), data)
        self.assertRedirects(response, reverse('lista_inscripciones'))
        resultado = Resultado.objects.get(inscripcion=self.inscripcion_cert)
        self.assertEqual(resultado.nota, 'A2')
        self.assertEqual(resultado.notaO, 'A2')
        self.assertEqual(resultado.notaC, 'A2')
        self.assertEqual(resultado.notaE, 'A2')
        self.assertEqual(resultado.notaL, 'A2')

    def test_evaluar_certificacion_actualiza_nivel_usuario(self):
        self.client.login(username='profesor1', password='testpass123')
        data = {
            'inscripcion_id': self.inscripcion_cert.id,
            'nota_oral': 'B2',
            'nota_comprension': 'B2',
            'nota_escritura': 'B2',
            'nota_audicion': 'B2'
        }
        self.client.post(reverse('evaluar_certificacion'), data)
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.nivel, 'B2')

    def test_evaluar_certificacion_no_certificacion(self):
        self.client.login(username='profesor1', password='testpass123')
        inscripcion = self.inscripcion_curso
        data = {
            'inscripcion_id': inscripcion.id,
            'nota_oral': 'A2',
            'nota_comprension': 'A2',
            'nota_escritura': 'A2',
            'nota_audicion': 'A2'
        }
        response = self.client.post(reverse('evaluar_certificacion'), data)
        self.assertRedirects(response, reverse('lista_inscripciones'))
        # No debe crear resultado ni cambiar nivel
        self.assertFalse(Resultado.objects.filter(inscripcion=inscripcion, notaO='A2').exists())