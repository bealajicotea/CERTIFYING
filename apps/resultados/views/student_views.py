from django.shortcuts import render, redirect
from gestion.models import  Resultado
from django.contrib import messages


def mis_resultados_estudiante(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    resultados = Resultado.objects.filter(inscripcion__estudiante_id=request.user.id)
    return render(request, 'rol_estudiante/lista_resultados_e.html', {'resultados': resultados})