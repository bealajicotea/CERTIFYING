from django.shortcuts import render, redirect, get_object_or_404
from apps.convocatorias.models import Convocatoria
from apps.notificaciones.models import Notification
from apps.inscripciones.models import Inscripcion
from apps.usuarios.models import Usuario
from django.contrib import messages
from django.db.models import Q

# --- Funciones auxiliares de filtrado y búsqueda para Convocatoria ---

def filtrar_convocatorias(filtros):
    """
    Filtra convocatorias por campos exactos.
    """
    convocatorias = Convocatoria.objects.select_related('profesor').all()

    tipo_convocatoria = filtros.get('tipo_convocatoria', '')
    nivel = filtros.get('nivel', '')
    lugar = filtros.get('lugar', '')
    fecha = filtros.get('fecha', '')
    profesor = filtros.get('profesor', '')

    if tipo_convocatoria:
        convocatorias = convocatorias.filter(tipo=tipo_convocatoria)
    if nivel:
        convocatorias = convocatorias.filter(nivel=nivel)
    if lugar:
        convocatorias = convocatorias.filter(lugar=lugar)
    if fecha:
        convocatorias = convocatorias.filter(fecha=fecha)
    if profesor:
        convocatorias = convocatorias.filter(profesor_id=profesor)

    return convocatorias

def buscar_en_convocatorias(convocatorias, buscar):
    """
    Busca en las convocatorias filtradas por varios campos.
    """
    if buscar:
        return convocatorias.filter(
            Q(descripcion__icontains=buscar) |
            Q(lugar__icontains=buscar) |
            Q(fecha__icontains=buscar) |
            Q(hora__icontains=buscar) |
            Q(profesor__username__icontains=buscar) |
            Q(tipo__icontains=buscar) |
            Q(nivel__icontains=buscar)
        )
    return convocatorias

def obtener_convocatorias_filtradas(filtros):
    """
    Aplica primero el filtrado y luego la búsqueda.
    """
    convocatorias = filtrar_convocatorias(filtros)
    buscar = filtros.get('buscar', '')
    convocatorias = buscar_en_convocatorias(convocatorias, buscar)

    tipos_convocatoria = Convocatoria.TIPO_CONVOCATORIA
    niveles = Convocatoria.niveles
    lugares = Convocatoria.lugares
    # Profesores: solo los usuarios tipo profesor
    profesores = Usuario.objects.filter(tipo_usuario='profesor').values_list('id', 'username')

    contexto = {
        'convocatorias': convocatorias,
        'tipos_convocatoria': tipos_convocatoria,
        'niveles': niveles,
        'lugares': lugares,
        'profesores': profesores,
        'selected_tipo_convocatoria': filtros.get('tipo_convocatoria', ''),
        'selected_nivel': filtros.get('nivel', ''),
        'selected_lugar': filtros.get('lugar', ''),
        'selected_fecha': filtros.get('fecha', ''),
        'selected_profesor': filtros.get('profesor', ''),
        'buscar': buscar,
    }
    return contexto

# --- Vistas ---

def lista_convocatorias(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    filtros = {
        'tipo_convocatoria': request.GET.get('tipo_convocatoria', ''),
        'nivel': request.GET.get('nivel', ''),
        'lugar': request.GET.get('lugar', ''),
        'fecha': request.GET.get('fecha', ''),
        'profesor': request.GET.get('profesor', ''),
        'buscar': request.GET.get('buscar', ''),
    }
    filtros_activos = request.GET.get('filtros_activos', '')
    contexto = obtener_convocatorias_filtradas(filtros)
    contexto['filtros_activos'] = filtros_activos
    return render(request, 'convocatorias/lista_convocatorias.html', contexto)

def crear_convocatoria(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == 'POST':
        data = request.POST
        convocatoria = Convocatoria(
            tipo=data.get('tipo'),
            descripcion=data.get('descripcion'),
            lugar=data.get('lugar'),
            fecha=data.get('fecha'),
            hora=data.get('hora'),
            nivel=data.get('nivel') or None,
            profesor=request.user,
            estado=True if data.get('estado') == 'on' else False,
        )
        convocatoria.save()
        Notification.objects.create(
            verb=f"Se ha creado una nueva {convocatoria.tipo} :",
            url=f"/convocatorias_e/detalle/{convocatoria.id}/"
        )
        # Inscribir automáticamente estudiantes de primer año si es de tipo colocacion
        if convocatoria.tipo == 'colocacion':
            estudiantes = Usuario.objects.filter(tipo_usuario='estudiante', anio_escolar='1')
            inscripciones = [
                Inscripcion(estudiante=est, convocatoria=convocatoria)
                for est in estudiantes
            ]
            Inscripcion.objects.bulk_create(inscripciones)
        messages.success(request, "Convocatoria creada exitosamente.")
        return redirect('lista_convocatorias')
    # Para el formulario, pasar los choices
    contexto = {
        'tipos_convocatoria': Convocatoria.TIPO_CONVOCATORIA,
        'niveles': Convocatoria.niveles,
        'lugares': Convocatoria.lugares,
        'profesores': Usuario.objects.filter(tipo_usuario='profesor'),
    }
    return render(request, 'convocatorias/crear_convocatoria.html', contexto)

def editar_convocatoria(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    if request.method == 'POST':
        data = request.POST
        convocatoria.tipo = data.get('tipo')
        convocatoria.descripcion = data.get('descripcion')
        convocatoria.lugar = data.get('lugar')
        convocatoria.fecha = data.get('fecha')
        convocatoria.hora = data.get('hora')
        convocatoria.nivel = data.get('nivel') or None
        convocatoria.estado = True if data.get('estado') == 'on' else False
        convocatoria.save()
        messages.success(request, "Convocatoria editada exitosamente.")
        return redirect('lista_convocatorias')
    contexto = {
        'convocatoria': convocatoria,
        'tipos_convocatoria': Convocatoria.TIPO_CONVOCATORIA,
        'niveles': Convocatoria.niveles,
        'lugares': Convocatoria.lugares,
        'profesores': Usuario.objects.filter(tipo_usuario='profesor'),
    }
    return render(request, 'convocatorias/editar_convocatoria.html', contexto)

def eliminar_convocatoria(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    convocatoria.delete()
    messages.success(request, "¡Convocatoria eliminada correctamente!")
    return redirect('lista_convocatorias')

def eliminar_convocatorias_seleccionadas(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == "POST":
        ids = request.POST.getlist('convocatorias_seleccionadas')
        if ids:
            Convocatoria.objects.filter(id__in=ids).delete()
            messages.success(request, "Convocatorias eliminadas exitosamente.")
        # Mantener filtros al volver a la lista
        filtros = {
            'tipo_convocatoria': request.POST.get('tipo_convocatoria', ''),
            'nivel': request.POST.get('nivel', ''),
            'lugar': request.POST.get('lugar', ''),
            'fecha': request.POST.get('fecha', ''),
            'profesor': request.POST.get('profesor', ''),
            'buscar': request.POST.get('buscar', ''),
        }
        filtros_activos = request.POST.get('filtros_activos', '')
        contexto = obtener_convocatorias_filtradas(filtros)
        contexto['filtros_activos'] = filtros_activos
        return render(request, 'convocatorias/lista_convocatorias.html', contexto)
    return redirect('lista_convocatorias')

def detalle_convocatoria(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    return render(request, 'convocatorias/detalle_convocatoria.html', {'convocatoria': convocatoria})