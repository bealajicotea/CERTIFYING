from django.shortcuts import render, redirect
from gestion.models import Convocatoria, Resultado

from django.contrib import messages

def lista_convocatorias_e(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    
    

    convocatorias = Convocatoria.objects.all()
    return render(request, 'rol_estudiante/lista_convocatorias_e.html', {'convocatorias': convocatorias})

def perfil_e(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    resultados = Resultado.objects.filter(inscripcion__estudiante=request.user).select_related('inscripcion__convocatoria')

    return render(request, 'rol_estudiante/perfil_e.html', {'resultados': resultados})