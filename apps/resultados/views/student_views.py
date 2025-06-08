from django.shortcuts import render, redirect
from apps.resultados.models import Resultado
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def lista_resultados_e(request):
    resultados = Resultado.objects.filter(inscripcion__estudiante_id=request.user.id)
    return render(request, 'rol_estudiante/lista_resultados_e.html', {'resultados': resultados})