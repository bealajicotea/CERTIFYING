from django.urls import path
from gestion.vistas import vista_usuario, vista_convocatoria, vista_resultado, vista_inscripcion

urlpatterns = [
    # URLs para Usuario
    path('usuarios/', vista_usuario.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', vista_usuario.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:usuario_id>/', vista_usuario.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', vista_usuario.eliminar_usuario, name='eliminar_usuario'),

    # URLs para Convocatoria
    path('convocatorias/', vista_convocatoria.lista_convocatorias, name='lista_convocatorias'),
    path('convocatorias/crear/', vista_convocatoria.crear_convocatoria, name='crear_convocatoria'),
    path('convocatorias/editar/<int:convocatoria_id>/', vista_convocatoria.editar_convocatoria, name='editar_convocatoria'),
    path('convocatorias/eliminar/<int:convocatoria_id>/', vista_convocatoria.eliminar_convocatoria, name='eliminar_convocatoria'),

    # URLs para Resultado
    path('resultados/', vista_resultado.lista_resultados, name='lista_resultados'),
    path('resultados/crear/', vista_resultado.crear_resultado, name='crear_resultado'),
    path('resultados/eliminar/<int:resultado_id>/', vista_resultado.eliminar_resultado, name='eliminar_resultado'),

    # URLs para Inscripcion
    path('inscripciones/', vista_inscripcion.lista_inscripciones, name='lista_inscripciones'),
    path('inscripciones/crear/', vista_inscripcion.crear_inscripcion, name='crear_inscripcion'),
    path('inscripciones/eliminar/<int:inscripcion_id>/', vista_inscripcion.eliminar_inscripcion, name='eliminar_inscripcion'),
]