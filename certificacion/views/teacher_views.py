from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from apps.convocatorias.models import Convocatoria
from apps.inscripciones.models import Inscripcion
from apps.resultados.models import Resultado
from django.db import models

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

    contexto = {
        'convocatorias_total': convocatorias.count(),
        'convocatorias_por_tipo': list(convocatorias_por_tipo),
        'inscripciones_total': inscripciones.count(),
        'inscripciones_por_estado': list(inscripciones_por_estado),
        'inscripciones_por_convocatoria': list(inscripciones_por_convocatoria),
        'resultados_total': resultados.count(),
        'resultados_por_nivel': list(resultados_por_nivel),
        'inicio_mes': inicio_mes,
        'fin_mes': fin_mes,
    }
    return render(request, 'reporte_mensual.html', contexto)
