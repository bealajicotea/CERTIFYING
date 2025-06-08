from django.urls import path
from apps.convocatorias.views import teacher_views,student_views

urlpatterns = [

    # URLs para Convocatoria
    path('convocatorias/', teacher_views.lista_convocatorias, name='lista_convocatorias'),
    path('convocatorias/crear/', teacher_views.crear_convocatoria, name='crear_convocatoria'),
    path('convocatorias/editar/<int:convocatoria_id>/', teacher_views.editar_convocatoria, name='editar_convocatoria'),
    path('convocatorias/eliminar/<int:convocatoria_id>/', teacher_views.eliminar_convocatoria, name='eliminar_convocatoria'),
    path('convocatorias/eliminar-seleccionadas/', teacher_views.eliminar_convocatorias_seleccionadas, name='eliminar_convocatorias_seleccionadas'),
    path('convocatorias/detalle/<int:convocatoria_id>/', teacher_views.detalle_convocatoria, name='detalle_convocatoria'),
    path('convocatorias_e/detalle/<int:convocatoria_id>/', student_views.detalle_convocatoriae, name='detalle_convocatoriae'),
    path('convocatorias_e/', student_views.lista_convocatorias_e, name='lista_convocatorias_e'),
    
    
    
    path('convocatorias_e/', student_views.lista_convocatorias_e, name='lista_convocatorias_e'),
    
]