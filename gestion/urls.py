from django.urls import path
from gestion.vistas import vista_usuario, vista_convocatoria, vista_resultado, vista_inscripcion,vistas_rol_estudiante

urlpatterns = [

    # URLs para Usuario
    path('usuarios/', vista_usuario.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', vista_usuario.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:usuario_id>/', vista_usuario.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', vista_usuario.eliminar_usuario, 
    name='eliminar_usuario'),
    path('usuarios/eliminar-seleccionados/',vista_usuario.eliminar_usuarios_seleccionados, name='eliminar_usuarios_seleccionados'),
    path('usuarios/detalle/<int:usuario_id>/', vista_usuario.detalle_usuario, name='detalle_usuario'),


    # URLs para Convocatoria
    path('convocatorias/', vista_convocatoria.lista_convocatorias, name='lista_convocatorias'),
    path('convocatorias/crear/', vista_convocatoria.crear_convocatoria, name='crear_convocatoria'),
    path('convocatorias/editar/<int:convocatoria_id>/', vista_convocatoria.editar_convocatoria, name='editar_convocatoria'),
    path('convocatorias/eliminar/<int:convocatoria_id>/', vista_convocatoria.eliminar_convocatoria, name='eliminar_convocatoria'),
    path('convocatorias/eliminar-seleccionadas/', vista_convocatoria.eliminar_convocatorias_seleccionadas, name='eliminar_convocatorias_seleccionadas'),
    path('convocatorias/detalle/<int:convocatoria_id>/', vista_convocatoria.detalle_convocatoria, name='detalle_convocatoria'),

    # URLs para Resultado
    path('resultados/', vista_resultado.lista_resultados, name='lista_resultados'),
    path('resultados/crear/', vista_resultado.crear_resultado, name='crear_resultado'),
    path('resultados/editar/<int:resultado_id>/', vista_resultado.editar_resultado, name='editar_resultado'),
    path('resultados/eliminar/<int:resultado_id>/', vista_resultado.eliminar_resultado, name='eliminar_resultado'),
    path('resultados/eliminar-seleccionados/', vista_resultado.eliminar_resultados_seleccionados, name='eliminar_resultados_seleccionados'),
    path('resultados/detalle/<int:resultado_id>/', vista_resultado.detalle_resultado, name='detalle_resultado'),
    

    # URLs para Inscripcion
    path('inscripciones/', vista_inscripcion.lista_inscripciones, name='lista_inscripciones'),
    path('inscripciones/crear/', vista_inscripcion.crear_inscripcion, name='crear_inscripcion'),
    path('inscripciones/editar/<int:inscripcion_id>/', vista_inscripcion.editar_inscripcion, name='editar_inscripcion'),
    path('inscripciones/eliminar/<int:inscripcion_id>/', vista_inscripcion.eliminar_inscripcion, name='eliminar_inscripcion'),
    path('inscripciones/eliminar-seleccionadas/', vista_inscripcion.eliminar_inscripciones_seleccionadas, name='eliminar_inscripciones_seleccionadas'),
    path('inscripciones/detalle/<int:inscripcion_id>/', vista_inscripcion.detalle_inscripcion, name='detalle_inscripcion'),
    path('resultados/evaluar/<int:inscripcion_id>/<str:nota>/', vista_inscripcion.evaluar, name='evaluar_resultado'),
    path('inscripciones/evaluar/', vista_inscripcion.evaluarInscripcion, name='evaluar_inscripcion'),

    path('convocatorias_e/', vistas_rol_estudiante.lista_convocatorias_e, name='lista_convocatorias_e'),
    path('perfil_e/', vistas_rol_estudiante.perfil_e, name='perfil_e'),

    
    path('resultados_e/', vistas_rol_estudiante.mis_resultados_estudiante, name='lista_resultados_e'),

    # URL para editar perfil
    path('editar_perfil/', vista_usuario.editar_perfil, name='editar_perfil'),

]