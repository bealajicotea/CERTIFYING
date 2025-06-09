from django.shortcuts import render, redirect, get_object_or_404
from apps.inscripciones.models import Inscripcion
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError  # Asegúrate de tener esta importación

def filtrar_inscripciones(filtros):
    """
    Filtra inscripciones por campos exactos.
    """
    inscripciones = Inscripcion.objects.select_related('estudiante', 'convocatoria').all()

    facultad = filtros.get('facultad', '')
    grupo = filtros.get('grupo', '')
    anio_escolar = filtros.get('anio_escolar', '')
    tipo_convocatoria = filtros.get('tipo_convocatoria', '')
    nivel = filtros.get('nivel', '')

    if facultad:
        inscripciones = inscripciones.filter(estudiante__facultad__icontains=facultad)
    if grupo:
        inscripciones = inscripciones.filter(estudiante__grupo__icontains=grupo)
    if anio_escolar:
        inscripciones = inscripciones.filter(estudiante__anio_escolar=anio_escolar)
    if tipo_convocatoria:
        inscripciones = inscripciones.filter(convocatoria__tipo=tipo_convocatoria)
    if nivel:
        inscripciones = inscripciones.filter(convocatoria__nivel=nivel)

    return inscripciones

def buscar_en_inscripciones(inscripciones, buscar):
    """
    Busca en los inscripciones filtrados por varios campos.
    """
    if buscar:
        return inscripciones.filter(
            Q(estudiante__username__icontains=buscar) |
            Q(convocatoria__tipo__icontains=buscar) |
            Q(fecha_inscripcion__icontains=buscar)
        )
    return inscripciones

def obtener_inscripciones_filtradas(filtros):
    """
    Aplica primero el filtrado y luego la búsqueda.
    """
    inscripciones = filtrar_inscripciones(filtros)
    buscar = filtros.get('buscar', '')
    inscripciones = buscar_en_inscripciones(inscripciones, buscar)

    # Obtener todas las opciones posibles desde los choices del modelo
    facultades = Usuario.fac if hasattr(Usuario, 'fac') else []
    grupos = Usuario.group if hasattr(Usuario, 'group') else []
    anios = Usuario.anios if hasattr(Usuario, 'anios') else []
    tipos_convocatoria = Convocatoria.TIPO_CONVOCATORIA
    niveles = Convocatoria.niveles

    contexto = {
        'inscripciones': inscripciones,
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
    }
    return contexto

def lista_inscripciones(request):
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
    }
    filtros_activos = request.GET.get('filtros_activos', '')
    contexto = obtener_inscripciones_filtradas(filtros)
    contexto['filtros_activos'] = filtros_activos
    return render(request, 'inscripciones/lista_inscripciones.html', contexto)

def crear_inscripcion(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    estudiantes = Usuario.objects.filter(tipo_usuario='estudiante')
    convocatorias = Convocatoria.objects.all()
    if request.method == 'POST':
        data = request.POST
        inscripcion = Inscripcion(
            estudiante_id=data.get('estudiante'),
            convocatoria_id=data.get('convocatoria'),
            estado=data.get('estado')
        )
        try:
            inscripcion.save()
            messages.success(request, "Inscripción creada exitosamente.")
            return redirect('lista_inscripciones')
        except IntegrityError:
            messages.error(request, "¡Alerta! Ya existe una inscripción para este estudiante y convocatoria.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al crear la inscripción: {e}")
    return render(request, 'inscripciones/crear_inscripcion.html', {
        'estudiantes': estudiantes,
        'convocatorias': convocatorias
    })

def eliminar_inscripcion(request, inscripcion_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    inscripcion.delete()
    return redirect('lista_inscripciones')

def eliminar_inscripciones_seleccionadas(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    # Procesar agregar nota
    if request.method == "POST":
        ids = request.POST.getlist('inscripciones_seleccionadas')
        if ids:
            Inscripcion.objects.filter(id__in=ids).delete()
        filtros = {
            'facultad': request.GET.get('facultad', ''),
            'grupo': request.GET.get('grupo', ''),
            'anio_escolar': request.GET.get('anio_escolar', ''),
            'tipo_convocatoria': request.GET.get('tipo_convocatoria', ''),
            'nivel': request.GET.get('nivel', ''),
        }
        contexto = obtener_inscripciones_filtradas(filtros)
        return render(request, 'inscripciones/lista_inscripciones.html', contexto)
    # Si no es POST, redirigir a la lista de inscripciones
    return redirect('lista_inscripciones')

def editar_inscripcion(request, inscripcion_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    estudiantes = Usuario.objects.filter(tipo_usuario='estudiante')
    convocatorias = Convocatoria.objects.all()
    if request.method == 'POST':
        data = request.POST
        inscripcion.estudiante_id = data.get('estudiante')
        inscripcion.convocatoria_id = data.get('convocatoria')
        inscripcion.estado = data.get('estado')
        inscripcion.save()
        messages.success(request, "Inscripción editada exitosamente.")
        return redirect('lista_inscripciones')
    return render(request, 'inscripciones/editar_inscripcion.html', {
        'inscripcion': inscripcion,
        'estudiantes': estudiantes,
        'convocatorias': convocatorias
    })

def detalle_inscripcion(request, inscripcion_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    return render(request, 'inscripciones/detalle_inscripcion.html', {'inscripcion': inscripcion})

def evaluar(inscripcion_id, nota):
    """
    Crea un resultado para la inscripción dada con la nota proporcionada.
    """
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    # Evita duplicados: si ya existe resultado, puedes actualizarlo o retornar
    if hasattr(inscripcion, 'resultado'):
        # Si quieres actualizar la nota existente:
        resultado = inscripcion.resultado
        resultado.nota = nota
        resultado.save()
    else:
        Resultado.objects.create(inscripcion=inscripcion, nota=nota)

def evaluarInscripcion(request):
    """
    Vista para evaluar una inscripción desde un formulario oculto.
    Espera recibir 'elemento_id' (id de la inscripción), 'codigo' (nota)
    y los filtros de búsqueda para mantenerlos tras la acción.
    """
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    # Recuperar los filtros del POST
    filtros = {
        'facultad': request.POST.get('facultad', ''),
        'grupo': request.POST.get('grupo', ''),
        'anio_escolar': request.POST.get('anio_escolar', ''),
        'tipo_convocatoria': request.POST.get('tipo_convocatoria', ''),
        'nivel': request.POST.get('nivel', ''),
    }

    if request.method == "POST":
        inscripcion_id = request.POST.get('elemento_id')
        nota = request.POST.get('codigo')

        if not inscripcion_id or not nota:
            messages.error(request, "Datos incompletos para evaluar la inscripción.")
            contexto = obtener_inscripciones_filtradas(filtros)
            return render(request, 'inscripciones/lista_inscripciones.html', contexto)

        inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
        # Evita duplicados: si ya existe resultado, actualiza; si no, crea
        if hasattr(inscripcion, 'resultado'):
            resultado = inscripcion.resultado
            resultado.nota = nota
            resultado.save()
            messages.success(request, "Nota actualizada correctamente.")
        else:
            Resultado.objects.create(inscripcion=inscripcion, nota=nota)
            messages.success(request, "Nota registrada correctamente.")

    # Siempre devolver la lista con el filtrado actual
    contexto = obtener_inscripciones_filtradas(filtros)
    return render(request, 'inscripciones/lista_inscripciones.html', contexto)