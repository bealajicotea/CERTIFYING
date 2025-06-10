from django.shortcuts import render, redirect
from apps.resultados.models import Resultado
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
def lista_resultados_e(request):
    resultados = Resultado.objects.filter(inscripcion__estudiante_id=request.user.id)
    # Paginación
    page_number = request.GET.get('page', 1)
    paginator = Paginator(resultados, 6)  # 10 por página
    page_obj = paginator.get_page(page_number)
    return render(request, 'rol_estudiante/lista_resultados_e.html', {
        'resultados': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })