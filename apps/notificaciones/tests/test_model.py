from django.test import TestCase
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.notificaciones.models import Notification

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user1 = Usuario.objects.create_user(
            username='user1',
            password='testpass123',
            tipo_usuario='estudiante'
        )
        self.user2 = Usuario.objects.create_user(
            username='user2',
            password='testpass123',
            tipo_usuario='profesor'
        )

    def test_crear_notificacion(self):
        notif = Notification.objects.create(
            verb="Nueva convocatoria disponible",
            url="https://ejemplo.com/convocatoria/1"
        )
        self.assertEqual(notif.verb, "Nueva convocatoria disponible")
        self.assertEqual(notif.url, "https://ejemplo.com/convocatoria/1")
        self.assertIsNotNone(notif.created_at)
        self.assertEqual(str(notif), f"Notificación: {notif.verb}")

    def test_url_opcional(self):
        notif = Notification.objects.create(
            verb="Sin URL"
        )
        self.assertIsNone(notif.url)

    def test_marcar_como_leida(self):
        notif = Notification.objects.create(
            verb="Notificación para leer"
        )
        notif.read_by.add(self.user1)
        self.assertIn(self.user1, notif.read_by.all())

    def test_varios_usuarios_leen(self):
        notif = Notification.objects.create(
            verb="Notificación para varios"
        )
        notif.read_by.add(self.user1, self.user2)
        self.assertIn(self.user1, notif.read_by.all())
        self.assertIn(self.user2, notif.read_by.all())

    def test_created_at_auto(self):
        notif = Notification.objects.create(
            verb="Verificar fecha"
        )
        self.assertIsNotNone(notif.created_at)