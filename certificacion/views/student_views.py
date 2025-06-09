from django.shortcuts import render
from apps.notificaciones.models import Notification

def index_view_e(request):
    user = request.user
    unread_notifications = Notification.objects.exclude(read_by=user)
    return render(
        request,
        'rol_estudiante/pagina_principal_e.html',
        {'notificaciones': unread_notifications}
    )