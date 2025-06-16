from django.test import TestCase, Client
from django.urls import reverse
from apps.usuarios.models import Usuario

class UsuarioViewsTest(TestCase):
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

    def test_lista_usuarios_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        response = self.client.get(reverse('lista_usuarios'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/lista_usuarios.html')
        self.assertIn('usuarios', response.context)

    def test_crear_usuario_get(self):
        response = self.client.get(reverse('crear_usuario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/crear_usuario.html')

    def test_crear_usuario_post(self):
        data = {
            'username': 'nuevo',
            'password': 'testpass123',
            'email': 'nuevo@correo.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'tipo_usuario': 'estudiante'
        }
        response = self.client.post(reverse('crear_usuario'), data)
        self.assertRedirects(response, reverse('lista_usuarios'))
        self.assertTrue(Usuario.objects.filter(username='nuevo').exists())

    def test_editar_usuario_requires_login(self):
        response = self.client.get(reverse('editar_usuario', args=[self.estudiante.id]))
        self.assertRedirects(response, reverse('login'))

    def test_editar_usuario_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('editar_usuario', args=[self.estudiante.id]))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_editar_usuario_post(self):
        self.client.login(username='profesor1', password='testpass123')
        data = {
            'username': 'editado',
            'email': 'editado@correo.com',
            'first_name': 'Editado',
            'last_name': 'Usuario',
            'tipo_usuario': 'estudiante'
        }
        response = self.client.post(reverse('editar_usuario', args=[self.estudiante.id]), data)
        self.assertRedirects(response, reverse('lista_usuarios'))
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.username, 'editado')

    def test_eliminar_usuario_requires_login(self):
        response = self.client.get(reverse('eliminar_usuario', args=[self.estudiante.id]))
        self.assertRedirects(response, reverse('login'))

    def test_eliminar_usuario_requires_profesor(self):
        self.client.login(username='estudiante1', password='testpass123')
        response = self.client.get(reverse('eliminar_usuario', args=[self.estudiante.id]))
        self.assertRedirects(response, reverse('pagina_principal'))

    def test_eliminar_usuario_profesor_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        response = self.client.get(reverse('eliminar_usuario', args=[self.estudiante.id]))
        self.assertRedirects(response, reverse('lista_usuarios'))
        self.assertFalse(Usuario.objects.filter(id=self.estudiante.id).exists())

    def test_eliminar_usuarios_seleccionados_post(self):
        self.client.login(username='profesor1', password='testpass123')
        user2 = Usuario.objects.create_user(
            username='user2',
            password='testpass123',
            tipo_usuario='estudiante'
        )
        data = {'usuarios_seleccionados': [self.estudiante.id, user2.id]}
        response = self.client.post(reverse('eliminar_usuarios_seleccionados'), data)
        self.assertRedirects(response, reverse('lista_usuarios'))
        self.assertFalse(Usuario.objects.filter(id=self.estudiante.id).exists())
        self.assertFalse(Usuario.objects.filter(id=user2.id).exists())

    def test_detalle_usuario_requires_login(self):
        response = self.client.get(reverse('detalle_usuario', args=[self.estudiante.id]))
        self.assertRedirects(response, reverse('login'))

    def test_detalle_usuario_ok(self):
        self.client.login(username='profesor1', password='testpass123')
        response = self.client.get(reverse('detalle_usuario', args=[self.estudiante.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/detalle_usuario.html')