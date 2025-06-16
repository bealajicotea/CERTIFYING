from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria

class TeacherViewsTest(TestCase):
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

    def test_lista_convocatorias_requires_login(self):
        response = self.client.get(reverse('lista_convocatorias'))
        self.assertRedirects(response, reverse('login'))

    def test_lista_convocatorias_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('lista_convocatorias'))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_lista_convocatorias_profesor_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        response = self.client.get(reverse('lista_convocatorias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'convocatorias/lista_convocatorias.html')
        self.assertIn('convocatorias', response.context)

    def test_crear_convocatoria_requires_login(self):
        response = self.client.get(reverse('crear_convocatoria'))
        self.assertRedirects(response, reverse('login'))

    def test_crear_convocatoria_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('crear_convocatoria'))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_crear_convocatoria_post(self):
        self.client.login(username='profesor1', password='testpass123')
        data = {
            'tipo': 'curso',
            'descripcion': 'Nueva convocatoria',
            'lugar': 'Docente 2',
            'fecha': timezone.now().date(),
            'hora': '10:00',
            'nivel': 'A1',
            'estado': 'on'
        }
        response = self.client.post(reverse('crear_convocatoria'), data)
        self.assertRedirects(response, reverse('lista_convocatorias'))
        self.assertTrue(Convocatoria.objects.filter(descripcion='Nueva convocatoria').exists())

    def test_editar_convocatoria_requires_login(self):
        response = self.client.get(reverse('editar_convocatoria', args=[self.convocatoria.id]))
        self.assertRedirects(response, reverse('login'))

    def test_editar_convocatoria_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('editar_convocatoria', args=[self.convocatoria.id]))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_eliminar_convocatoria_requires_login(self):
        response = self.client.get(reverse('eliminar_convocatoria', args=[self.convocatoria.id]))
        self.assertRedirects(response, reverse('login'))

    def test_eliminar_convocatoria_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('eliminar_convocatoria', args=[self.convocatoria.id]))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_detalle_convocatoria_requires_login(self):
        response = self.client.get(reverse('detalle_convocatoria', args=[self.convocatoria.id]))
        self.assertRedirects(response, reverse('login'))

    def test_detalle_convocatoria_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        response = self.client.get(reverse('detalle_convocatoria', args=[self.convocatoria.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'convocatorias/detalle_convocatoria.html')
        self.assertEqual(response.context['convocatoria'], self.convocatoria)