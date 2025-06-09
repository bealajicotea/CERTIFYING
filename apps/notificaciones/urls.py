from django.urls import path
from apps.notificaciones.views import student_views

urlpatterns = [
    # URLs para Notificaciones
    path('lista/notificaciones/', student_views.notificaciones, name='lista_notificaciones'),
    path('leer/notificacion/<int:pk>/', student_views.marcar_como_leida, name='leer_notificacion'),
]