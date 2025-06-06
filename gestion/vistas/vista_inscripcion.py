from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from gestion.models import Inscripcion, Usuario, Resultado, Convocatoria
from gestion.forms import InscripcionForm
from django.contrib import messages
from django.db.models import Q

def obtener_inscripciones_filtradas(filtros):
    """
    Recibe un diccionario de filtros y retorna:
    - queryset filtrado de inscripciones
    - diccionario de contexto para el render
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

    facultades = Usuario.objects.filter(tipo_usuario='estudiante').values_list('facultad', flat=True).distinct()
    grupos = Usuario.objects.filter(tipo_usuario='estudiante').values_list('grupo', flat=True).distinct()
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
        'selected_facultad': facultad,
        'selected_grupo': grupo,
        'selected_anio': anio_escolar,
        'selected_tipo_convocatoria': tipo_convocatoria,
        'selected_nivel': nivel,
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
    }

    contexto = obtener_inscripciones_filtradas(filtros)

    return render(request, 'inscripciones/lista_inscripciones.html', contexto)

def crear_inscripcion(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_inscripciones')
    else:
        form = InscripcionForm()
    return render(request, 'inscripciones/crear_inscripcion.html', {'form': form})

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
    if request.method == 'POST':
        form = InscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            form.save()
            return redirect('lista_inscripciones')
    else:
        form = InscripcionForm(instance=inscripcion)
    return render(request, 'inscripciones/editar_inscripcion.html', {'form': form})

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