from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria
from apps.inscripciones.models import Inscripcion
from apps.resultados.models import Resultado

class InscripcionesTeacherViewsTest(TestCase):
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
        self.convocatoria = Convocatoria.objects.create(
            tipo='certificacion',
            descripcion='Convocatoria de prueba',
            lugar='Docente 1',
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            profesor=self.profesor,
            nivel='A2'
        )
        self.inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            convocatoria=self.convocatoria
        )

    def test_lista_inscripciones_requires_login(self):
        response = self.client.get(reverse('lista_inscripciones'))
        self.assertRedirects(response, reverse('login'))

    def test_lista_inscripciones_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('lista_inscripciones'))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_lista_inscripciones_profesor_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        response = self.client.get(reverse('lista_inscripciones'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscripciones/lista_inscripciones.html')
        self.assertIn('inscripciones', response.context)

    def test_crear_inscripcion_requires_login(self):
        response = self.client.get(reverse('crear_inscripcion'))
        self.assertRedirects(response, reverse('login'))

    def test_crear_inscripcion_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('crear_inscripcion'))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_crear_inscripcion_post(self):
        self.client.login(username='profesor1', password='testpass123')
        estudiante2 = Usuario.objects.create_user(
            username='estudiante2',
            password='testpass123',
            tipo_usuario='estudiante'
        )
        data = {
            'estudiante': estudiante2.id,
            'convocatoria': self.convocatoria.id,
            'estado': 'pendiente'
        }
        response = self.client.post(reverse('crear_inscripcion'), data)
        self.assertRedirects(response, reverse('lista_inscripciones'))
        self.assertTrue(Inscripcion.objects.filter(estudiante=estudiante2, convocatoria=self.convocatoria).exists())

    def test_eliminar_inscripcion_requires_login(self):
        response = self.client.get(reverse('eliminar_inscripcion', args=[self.inscripcion.id]))
        self.assertRedirects(response, reverse('login'))

    def test_eliminar_inscripcion_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('eliminar_inscripcion', args=[self.inscripcion.id]))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_eliminar_inscripcion_profesor_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        response = self.client.get(reverse('eliminar_inscripcion', args=[self.inscripcion.id]))
        self.assertRedirects(response, reverse('lista_inscripciones'))
        self.assertFalse(Inscripcion.objects.filter(id=self.inscripcion.id).exists())

    def test_editar_inscripcion_requires_login(self):
        response = self.client.get(reverse('editar_inscripcion', args=[self.inscripcion.id]))
        self.assertRedirects(response, reverse('login'))

    def test_editar_inscripcion_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('editar_inscripcion', args=[self.inscripcion.id]))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_editar_inscripcion_profesor_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        estudiante2 = Usuario.objects.create_user(
            username='estudiante2',
            password='testpass123',
            tipo_usuario='estudiante'
        )
        data = {
            'estudiante': estudiante2.id,
            'convocatoria': self.convocatoria.id,
            'estado': 'aprobado'
        }
        response = self.client.post(reverse('editar_inscripcion', args=[self.inscripcion.id]), data)
        self.assertRedirects(response, reverse('lista_inscripciones'))
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estudiante, estudiante2)
        self.assertEqual(self.inscripcion.estado, 'aprobado')

    def test_detalle_inscripcion_requires_login(self):
        response = self.client.get(reverse('detalle_inscripcion', args=[self.inscripcion.id]))
        self.assertRedirects(response, reverse('login'))

    def test_detalle_inscripcion_profesor_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        response = self.client.get(reverse('detalle_inscripcion', args=[self.inscripcion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscripciones/detalle_inscripcion.html')
        self.assertEqual(response.context['inscripcion'], self.inscripcion)

    def test_evaluarInscripcion_post(self):
        self.client.login(username='profesor1', password='testpass123')
        data = {
            'elemento_id': self.inscripcion.id,
            'codigo': 'A2'
        }
        response = self.client.post(reverse('evaluar_inscripcion'), data)
        self.assertRedirects(response, reverse('lista_inscripciones'))
        resultado = Resultado.objects.get(inscripcion=self.inscripcion)
        self.assertEqual(resultado.nota, 'A2')

    def test_evaluar_certificacion_post(self):
        self.client.login(username='profesor1', password='testpass123')
        data = {
            'inscripcion_id': self.inscripcion.id,
            'nota_oral': 'A2',
            'nota_comprension': 'A2',
            'nota_escritura': 'A2',
            'nota_audicion': 'A2'
        }
        response = self.client.post(reverse('evaluar_certificacion'), data)
        self.assertRedirects(response, reverse('lista_inscripciones'))
        resultado = Resultado.objects.get(inscripcion=self.inscripcion)
        self.assertEqual(resultado.nota, 'A2')
        self.inscripcion.estudiante.refresh_from_db()
        self.assertEqual(self.inscripcion.estudiante.nivel, 'A2')