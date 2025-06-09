from django.urls import path
from apps.inscripciones.views import teacher_views
from .views.teacher_views import evaluar_certificacion


urlpatterns = [
    # URLs para Inscripcion
    path('inscripciones/', teacher_views.lista_inscripciones, name='lista_inscripciones'),
    path('inscripciones/crear/', teacher_views.crear_inscripcion, name='crear_inscripcion'),
    path('inscripciones/editar/<int:inscripcion_id>/', teacher_views.editar_inscripcion, name='editar_inscripcion'),
    path('inscripciones/eliminar/<int:inscripcion_id>/', teacher_views.eliminar_inscripcion, name='eliminar_inscripcion'),
    path('inscripciones/eliminar-seleccionadas/', teacher_views.eliminar_inscripciones_seleccionadas, name='eliminar_inscripciones_seleccionadas'),
    path('inscripciones/detalle/<int:inscripcion_id>/', teacher_views.detalle_inscripcion, name='detalle_inscripcion'),
    path('resultados/evaluar/<int:inscripcion_id>/<str:nota>/', teacher_views.evaluar, name='evaluar_resultado'),
    path('inscripciones/evaluar/', teacher_views.evaluarInscripcion, name='evaluar_inscripcion'),
    path('evaluar_certificacion/', evaluar_certificacion, name='evaluar_certificacion'),

]