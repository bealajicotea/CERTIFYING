from django.shortcuts import render, redirect, get_object_or_404
from apps.resultados.models import Resultado
from apps.inscripciones.models import Inscripcion
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

# --- Funciones auxiliares de filtrado y búsqueda para Resultado ---

def filtrar_resultados(filtros):
    """
    Filtra resultados por campos exactos relacionados.
    Si todos los filtros están vacíos, retorna todos los resultados.
    """
    resultados = Resultado.objects.select_related(
        'inscripcion__estudiante', 'inscripcion__convocatoria'
    ).all()

    facultad = filtros.get('facultad', '')
    grupo = filtros.get('grupo', '')
    anio_escolar = filtros.get('anio_escolar', '')
    tipo_convocatoria = filtros.get('tipo_convocatoria', '')
    nivel = filtros.get('nivel', '')

    if facultad:
        resultados = resultados.filter(inscripcion__estudiante__facultad=facultad)
    if grupo:
        resultados = resultados.filter(inscripcion__estudiante__grupo=grupo)
    if anio_escolar:
        resultados = resultados.filter(inscripcion__estudiante__anio_escolar=anio_escolar)
    if tipo_convocatoria:
        resultados = resultados.filter(inscripcion__convocatoria__tipo=tipo_convocatoria)
    if nivel:
        resultados = resultados.filter(inscripcion__convocatoria__nivel=nivel)

    return resultados

def buscar_en_resultados(resultados, buscar):
    """
    Busca en los resultados filtrados por varios campos.
    """
    if buscar:
        return resultados.filter(
            Q(inscripcion__estudiante__username__icontains=buscar) |
            Q(inscripcion__estudiante__first_name__icontains=buscar) |
            Q(inscripcion__estudiante__last_name__icontains=buscar) |
            Q(inscripcion__estudiante__facultad__icontains=buscar) |
            Q(inscripcion__estudiante__grupo__icontains=buscar) |
            Q(inscripcion__estudiante__anio_escolar__icontains=buscar) |
            Q(inscripcion__convocatoria__tipo__icontains=buscar) |
            Q(inscripcion__convocatoria__nivel__icontains=buscar) |
            Q(nota__icontains=buscar)
        )
    return resultados

def obtener_resultados_filtrados(filtros):
    """
    Aplica primero el filtrado y luego la búsqueda.
    """
    resultados = filtrar_resultados(filtros)
    buscar = filtros.get('buscar', '')
    resultados = buscar_en_resultados(resultados, buscar)

    facultades = Usuario.fac
    grupos = Usuario.group
    anios = Usuario.anios
    tipos_convocatoria = Convocatoria.TIPO_CONVOCATORIA
    niveles = Convocatoria.niveles

    contexto = {
        'resultados': resultados,
        'facultades': facultades,
        'grupos': grupos,
        'anios': anios,
        'tipos_convocatoria': tipos_convocatoria,
        'niveles': niveles,
        'selected_facultad': filtros.get('facultad', ''),
        'selected_grupo': filtros.get('grupo', ''),
        'selected_anio': filtros.get('anio_escolar', ''),
        'selected_tipo_convocatoria': filtros.get('tipo_convocatoria', ''),
        'selected_nivel': filtros.get('nivel', ''),
        'buscar': buscar,
        'filtros_activos': filtros.get('filtros_activos', ''),
    }
    return contexto

def lista_resultados(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    filtros = {
        'facultad': request.GET.get('facultad', ''),
        'grupo': request.GET.get('grupo', ''),
        'anio_escolar': request.GET.get('anio_escolar', ''),
        'tipo_convocatoria': request.GET.get('tipo_convocatoria', ''),
        'nivel': request.GET.get('nivel', ''),
        'buscar': request.GET.get('buscar', ''),
        'filtros_activos': request.GET.get('filtros_activos', ''),
    }
    contexto = obtener_resultados_filtrados(filtros)
    # Paginación
    resultados = contexto['resultados']
    page_number = request.GET.get('page', 1)
    paginator = Paginator(resultados, 6)  # 10 por página
    page_obj = paginator.get_page(page_number)
    contexto['resultados'] = page_obj
    contexto['page_obj'] = page_obj
    contexto['is_paginated'] = page_obj.has_other_pages()
    return render(request, 'resultados/lista_resultados.html', contexto)

def crear_resultado(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    inscripciones = Inscripcion.objects.all()
    profesores = Usuario.objects.filter(tipo_usuario='profesor')
    niveles = Resultado.NIVELES
    if request.method == 'POST':
        data = request.POST
        inscripcion_id = data.get('inscripcion')
        nivel = data.get('nivel')
        # Verifica si ya existe un resultado para esa inscripción
        if Resultado.objects.filter(inscripcion_id=inscripcion_id).exists():
            messages.error(request, "Ya existe un resultado para esta inscripción.")
        else:
            resultado = Resultado(
                inscripcion_id=inscripcion_id,
                nota=nivel
            )
            resultado.save()
            messages.success(request, "¡Resultado registrado exitosamente!")
            return redirect('lista_resultados')
    return render(request, 'resultados/crear_resultado.html', {
        'inscripciones': inscripciones,
        'profesores': profesores,
        'niveles': niveles
    })

def eliminar_resultado(request, resultado_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    resultado = get_object_or_404(Resultado, id=resultado_id)
    resultado.delete()
    messages.success(request, "El resultado fue eliminado correctamente.")
    return redirect('lista_resultados')

def eliminar_resultados_seleccionados(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == "POST":
        ids = request.POST.getlist('resultados_seleccionados')
        if ids:
            Resultado.objects.filter(id__in=ids).delete()
            messages.success(request, "Resultados eliminados correctamente.")
        else:
            messages.warning(request, "Seleccione al menos un resultado para eliminar.")
    return redirect('lista_resultados')

def editar_resultado(request, resultado_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    resultado = get_object_or_404(Resultado, id=resultado_id)
    inscripciones = Inscripcion.objects.all()
    niveles = Resultado.NIVELES
    if request.method == 'POST':
        data = request.POST
        resultado.inscripcion_id = data.get('inscripcion')
        resultado.nota = data.get('nivel')
        resultado.save()
        messages.success(request, "El resultado fue actualizado correctamente.")
        return redirect('lista_resultados')
    return render(request, 'resultados/editar_resultado.html', {
        'resultado': resultado,
        'inscripciones': inscripciones,
        'niveles': niveles
    })

def detalle_resultado(request, resultado_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    resultado = get_object_or_404(Resultado, id=resultado_id)
    return render(request, 'resultados/detalle_resultado.html', {'resultado': resultado})
