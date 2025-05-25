from django.shortcuts import render, redirect, get_object_or_404
from gestion.models import Convocatoria, Resultado, Inscripcion
from django.contrib import messages
from django.utils import timezone

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
                inscripcion, created = Inscripcion.objects.get_or_create(
                    estudiante=request.user,
                    convocatoria=convocatoria
                )
                if created:
                    mensaje = {'tipo': 'success', 'texto': 'Inscripción realizada correctamente.'}
                else:
                    mensaje = {'tipo': 'danger', 'texto': 'Ya estabas inscrito en esta convocatoria.'}
            except Exception as e:
                mensaje = {'tipo': 'danger', 'texto': f'Error al inscribirse: {str(e)}'}
        # No redirigir, solo mostrar mensaje en la misma página

    convocatorias = Convocatoria.objects.all()
    return render(request, 'rol_estudiante/lista_convocatorias_e.html', {'convocatorias': convocatorias, 'mensaje': mensaje})

def perfil_e(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    
    return render(request, 'rol_estudiante/perfil_e.html')

def mis_resultados_estudiante(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    resultados = Resultado.objects.filter(inscripcion__estudiante_id=request.user.id)
    return render(request, 'rol_estudiante/lista_resultados_e.html', {'resultados': resultados})