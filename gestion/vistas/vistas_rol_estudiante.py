from django.shortcuts import render, redirect
from gestion.models import Convocatoria

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
    
    return render(request, 'rol_estudiante/perfil_e.html', {})