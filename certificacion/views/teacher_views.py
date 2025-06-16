from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from apps.convocatorias.models import Convocatoria
from apps.inscripciones.models import Inscripcion
from apps.resultados.models import Resultado
from django.db import models
from django.core.paginator import Paginator

def index_view(request):
    return render(request, 'pagina_principal.html')

def reporte_mensual_view(request):
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Obtener filtros desde GET
    buscar = request.GET.get('buscar', '').strip()
    tipo_convocatoria = request.GET.get('tipo_convocatoria', '')
    estado_inscripcion = request.GET.get('estado_inscripcion', '')
    nivel = request.GET.get('nivel', '')

    # Todas las opciones posibles
    TODOS_TIPOS = [t[0] for t in Convocatoria.TIPO_CONVOCATORIA]
    TODOS_NIVELES = [n[0] for n in Convocatoria.niveles]
    TODOS_ESTADOS = list(Inscripcion.objects.values_list('estado', flat=True).distinct())

    # Filtrar convocatorias
    convocatorias = Convocatoria.objects.filter(fecha_creacion__date__gte=inicio_mes, fecha_creacion__date__lte=fin_mes)
    if tipo_convocatoria:
        convocatorias = convocatorias.filter(tipo=tipo_convocatoria)
    if buscar:
        convocatorias = convocatorias.filter(descripcion__icontains=buscar)
    convocatorias_por_tipo = convocatorias.values('tipo').order_by('tipo').annotate(total=models.Count('id'))

    # Filtrar inscripciones
    inscripciones = Inscripcion.objects.filter(fecha_creacion__date__gte=inicio_mes, fecha_creacion__date__lte=fin_mes)
    if estado_inscripcion:
        inscripciones = inscripciones.filter(estado=estado_inscripcion)
    if tipo_convocatoria:
        inscripciones = inscripciones.filter(convocatoria__tipo=tipo_convocatoria)
    if buscar:
        inscripciones = inscripciones.filter(
            models.Q(estudiante__username__icontains=buscar) |
            models.Q(convocatoria__descripcion__icontains=buscar)
        )
    inscripciones_por_estado = inscripciones.values('estado').order_by('estado').annotate(total=models.Count('id'))
    inscripciones_por_convocatoria = inscripciones.values('convocatoria__descripcion').annotate(total=models.Count('id'))

    # Filtrar resultados
    resultados = Resultado.objects.filter(fecha_creacion__date__gte=inicio_mes, fecha_creacion__date__lte=fin_mes)
    if nivel:
        resultados = resultados.filter(nota=nivel)
    if buscar:
        resultados = resultados.filter(
            models.Q(inscripcion__estudiante__username__icontains=buscar) |
            models.Q(inscripcion__convocatoria__descripcion__icontains=buscar)
        )
    resultados_por_nivel = resultados.values('nota').order_by('nota').annotate(total=models.Count('id'))

    # Paginación (6 por página para cada tabla)
    page_c = request.GET.get('page_c', 1)
    page_i = request.GET.get('page_i', 1)
    page_ic = request.GET.get('page_ic', 1)
    page_r = request.GET.get('page_r', 1)

    paginator_c = Paginator(list(convocatorias_por_tipo), 6)
    paginator_i = Paginator(list(inscripciones_por_estado), 6)
    paginator_ic = Paginator(list(inscripciones_por_convocatoria), 6)
    paginator_r = Paginator(list(resultados_por_nivel), 6)

    contexto = {
        'convocatorias_total': convocatorias.count(),
        'convocatorias_por_tipo': paginator_c.get_page(page_c),
        'inscripciones_total': inscripciones.count(),
        'inscripciones_por_estado': paginator_i.get_page(page_i),
        'inscripciones_por_convocatoria': paginator_ic.get_page(page_ic),
        'resultados_total': resultados.count(),
        'resultados_por_nivel': paginator_r.get_page(page_r),
        'inicio_mes': inicio_mes,
        'fin_mes': fin_mes,
        'todos_tipos': TODOS_TIPOS,
        'todos_niveles': TODOS_NIVELES,
        'todos_estados': TODOS_ESTADOS,
        'selected_tipo_convocatoria': tipo_convocatoria,
        'selected_nivel': nivel,
        'selected_estado_inscripcion': estado_inscripcion,
        'buscar': buscar,
        'paginator_c': paginator_c,
        'paginator_i': paginator_i,
        'paginator_ic': paginator_ic,
        'paginator_r': paginator_r,
    }
    return render(request, 'reporte_mensual.html', contexto)
