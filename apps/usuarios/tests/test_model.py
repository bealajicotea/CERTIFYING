from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.usuarios.models import Usuario

class UsuarioModelTest(TestCase):
    def test_usuario_creacion_estudiante(self):
        usuario = Usuario.objects.create_user(
            username='estudiante1',
            password='testpass123',
            tipo_usuario='estudiante',
            facultad='FTL',
            anio_escolar='1',
            grupo='1',
            carrera='Ingenieria en Ciencias Informáticas',
            curso='A1',
            nivel='A1'
        )
        self.assertEqual(usuario.username, 'estudiante1')
        self.assertTrue(usuario.es_estudiante())
        self.assertFalse(usuario.es_profesor())
        self.assertEqual(usuario.tipo_usuario, 'estudiante')
        self.assertEqual(str(usuario), "estudiante1 (estudiante)")

    def test_usuario_creacion_profesor(self):
        usuario = Usuario.objects.create_user(
            username='profesor1',
            password='testpass123',
            tipo_usuario='profesor',
        )
        self.assertEqual(usuario.username, 'profesor1')
        self.assertTrue(usuario.es_profesor())
        self.assertFalse(usuario.es_estudiante())
        self.assertEqual(usuario.tipo_usuario, 'profesor')
        self.assertEqual(str(usuario), "profesor1 (profesor)")

    def test_usuario_foto_perfil(self):
        usuario = Usuario.objects.create_user(
            username='con_foto',
            password='testpass123',
            tipo_usuario='estudiante'
        )
        foto = SimpleUploadedFile("foto.jpg", b"file_content", content_type="image/jpeg")
        usuario.foto_perfil = foto
        usuario.save()
        # El nombre real será algo como: fotos_perfil/user_1/foto_xxxxxxxx.jpg
        self.assertTrue(usuario.foto_perfil.name.startswith(f'fotos_perfil/user_{usuario.id}/'))
        self.assertTrue(usuario.foto_perfil.name.endswith('.jpg'))
        self.assertIn('foto', usuario.foto_perfil.name)

    def test_usuario_campos_opcionales(self):
        usuario = Usuario.objects.create_user(
            username='opcional',
            password='testpass123',
            tipo_usuario='estudiante'
        )
        self.assertIsNone(usuario.facultad)
        self.assertIsNone(usuario.anio_escolar)
        self.assertIsNone(usuario.carrera)
        self.assertIsNone(usuario.curso)
        self.assertIsNone(usuario.nivel)
        self.assertIsNone(usuario.foto_perfil.name)
