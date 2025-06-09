from django.shortcuts import render
from apps.notificaciones.models import Notification
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import io

def index_view_e(request):
    user = request.user
    unread_notifications = Notification.objects.exclude(read_by=user)
    return render(
        request,
        'rol_estudiante/pagina_principal_e.html',
        {'notificaciones': unread_notifications}
    )

def generar_certificado(request):
    template = get_template("rol_estudiante/plantilla_certificado.html")
    # Obtener el nombre completo del usuario actual
    nombre_completo = request.user.get_full_name() if hasattr(request.user, 'get_full_name') else str(request.user)
    context = {"nombre": nombre_completo}

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'

    # Crear el PDF en memoria
    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    return response