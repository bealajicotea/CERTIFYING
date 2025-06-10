from django.urls import path
from apps.resultados.views import teacher_views, student_views

urlpatterns = [
    # URLs para Resultado (profesor)
    path('resultados/', teacher_views.lista_resultados, name='lista_resultados'),
    path('resultados/crear/', teacher_views.crear_resultado, name='crear_resultado'),
    path('resultados/editar/<int:resultado_id>/', teacher_views.editar_resultado, name='editar_resultado'),
    path('resultados/eliminar/<int:resultado_id>/', teacher_views.eliminar_resultado, name='eliminar_resultado'),
    path('resultados/eliminar-seleccionados/', teacher_views.eliminar_resultados_seleccionados, name='eliminar_resultados_seleccionados'),
    path('resultados/detalle/<int:resultado_id>/', teacher_views.detalle_resultado, name='detalle_resultado'),
    
    # URLs para Resultado (estudiante)
    path('resultados_e/', student_views.lista_resultados_e, name='lista_resultados_e'),
]