from django.urls import path
from apps.usuarios.views import student_views,teacher_views, generic_views as views

urlpatterns = [
 # URLs para Usuario
    path('usuarios/', teacher_views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', teacher_views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:usuario_id>/', teacher_views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', teacher_views.eliminar_usuario, 
    name='eliminar_usuario'),
    path('usuarios/eliminar-seleccionados/',teacher_views.eliminar_usuarios_seleccionados, name='eliminar_usuarios_seleccionados'),
    path('usuarios/detalle/<int:usuario_id>/', teacher_views.detalle_usuario, name='detalle_usuario'),  
    path('perfil/', views.perfil, name='perfil'),  # Perfil profesor
    path('perfil_estudiante/', student_views.perfil_estudiante, name='perfil_estudiante'),  # Perfil estudiante
    path('editar/perfil/', views.editar_perfil, name='editar_perfil'),
    path('foto/', views.foto, name='foto'),
    path('editar_perfil_e/', student_views.editar_perfil_e, name='editar_perfil_e'),
]