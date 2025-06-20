from django.shortcuts import render, redirect, get_object_or_404
from apps.convocatorias.models import Convocatoria
from apps.inscripciones.models import Inscripcion
from django.contrib import messages
from django.core.paginator import Paginator

def lista_convocatorias_e(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')

    mensaje = None
    if request.method == 'POST':
        convocatoria_id = request.POST.get('convocatoria_id')
        if not convocatoria_id or not convocatoria_id.isdigit():
            mensaje = {'tipo': 'danger', 'texto': 'Solicitud inválida: convocatoria no especificada.'}
        else:
            try:
                convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
                # Restricción para certificación: solo A2 o superior
                if convocatoria.tipo == 'certificacion':
                    niveles_validos = ['A2', 'B1', 'B2', 'C1', 'C2']
                    if request.user.nivel not in niveles_validos:
                        mensaje = {
                            'tipo': 'danger',
                            'texto': 'Solo puedes inscribirte en certificaciones si tienes nivel A2 o superior.'
                        }
                    else:
                        inscripcion, created = Inscripcion.objects.get_or_create(
                            estudiante=request.user,
                            convocatoria=convocatoria
                        )
                        if created:
                            mensaje = {'tipo': 'success', 'texto': '¡Te has inscrito correctamente en la convocatoria!'}
                        else:
                            mensaje = {'tipo': 'danger', 'texto': 'Ya estás inscrito en esta convocatoria.'}
                else:
                    inscripcion, created = Inscripcion.objects.get_or_create(
                        estudiante=request.user,
                        convocatoria=convocatoria
                    )
                    if created:
                        mensaje = {'tipo': 'success', 'texto': '¡Te has inscrito correctamente en la convocatoria!'}
                    else:
                        mensaje = {'tipo': 'danger', 'texto': 'Ya estás inscrito en esta convocatoria.'}
            except Exception as e:
                mensaje = {'tipo': 'danger', 'texto': f'Ocurrió un error al inscribirse: {str(e)}'}
        # No redirigir, solo mostrar mensaje en la misma página

    convocatorias = Convocatoria.objects.all()
    # Paginación
    page_number = request.GET.get('page', 1)
    paginator = Paginator(convocatorias, 10)  # 10 por página
    page_obj = paginator.get_page(page_number)
    return render(request, 'rol_estudiante/lista_convocatorias_e.html', {
        'convocatorias': page_obj,
        'mensaje': mensaje,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })

def detalle_convocatoriae(request, convocatoria_id):
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    return render(request, 'rol_estudiante/detalle_convocatoriae.html', {'convocatoria': convocatoria})
