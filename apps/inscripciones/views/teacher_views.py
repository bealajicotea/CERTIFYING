from django.shortcuts import render, redirect, get_object_or_404
from apps.inscripciones.models import Inscripcion
from apps.usuarios.models import Usuario
from apps.convocatorias.models import Convocatoria
from apps.resultados.models import Resultado
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError  # Asegúrate de tener esta importación
from django.urls import reverse
from django.core.paginator import Paginator

from urllib.parse import urlencode


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
            Q(estudiante__first_name__icontains=buscar) |
            Q(estudiante__last_name__icontains=buscar) |
            Q(estudiante__facultad__icontains=buscar) |
            Q(estudiante__grupo__icontains=buscar) |
            Q(estudiante__anio_escolar__icontains=buscar) |
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

    # Paginación
    inscripciones = contexto['inscripciones']
    page_number = request.GET.get('page', 1)
    paginator = Paginator(inscripciones, 6)  # 10 por página
    page_obj = paginator.get_page(page_number)
    contexto['inscripciones'] = page_obj
    contexto['page_obj'] = page_obj
    contexto['is_paginated'] = page_obj.has_other_pages()

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
            messages.success(request, "¡Inscripción realizada correctamente! El estudiante ha sido inscrito en la convocatoria.")
            return redirect('lista_inscripciones')
        except IntegrityError:
            messages.error(request, "Este estudiante ya está inscrito en la convocatoria seleccionada.")
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
    messages.success(request, "La inscripción fue eliminada exitosamente.")
    return redirect('lista_inscripciones')

def eliminar_inscripciones_seleccionadas(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    
    if request.method == "POST":
        ids = request.POST.getlist('inscripciones_seleccionadas')
        if ids:
            Inscripcion.objects.filter(id__in=ids).delete()
            messages.success(request, "Inscripciones eliminadas correctamente.")
        else:
            messages.warning(request, "Debe seleccionar al menos una inscripción para eliminar.")
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
        messages.success(request, "La inscripción se actualizó correctamente.")
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
    resultado = getattr(inscripcion, 'resultado', None)
    if resultado is not None and resultado.nota == "A1":
        # Si quieres actualizar la nota existente:
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
        'buscar': request.POST.get('buscar', ''),
        'filtros_activos': request.POST.get('filtros_activos', ''),
    }

    if request.method == "POST":
        inscripcion_id = request.POST.get('elemento_id')
        nota = request.POST.get('codigo')

        if not inscripcion_id or not nota:
            messages.error(request, "Debe ingresar una nota válida para evaluar la inscripción.")
            contexto = obtener_inscripciones_filtradas(filtros)
            return render(request, 'inscripciones/lista_inscripciones.html', contexto)

        inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
        resultado = getattr(inscripcion, 'resultado', None)
        if resultado is not None:
            resultado.nota = nota
            resultado.save()
            messages.success(request, "La nota de la inscripción fue actualizada correctamente.")
        else:
            Resultado.objects.create(inscripcion=inscripcion, nota=nota)
            messages.success(request, "La nota fue registrada correctamente para la inscripción seleccionada.")

        # Redirigir a la lista de inscripciones con los filtros como parámetros GET
        query_string = urlencode({k: v for k, v in filtros.items() if v})
        return redirect(f"{reverse('lista_inscripciones')}?{query_string}")

    # Siempre devolver la lista con el filtrado actual
    contexto = obtener_inscripciones_filtradas(filtros)
    return render(request, 'inscripciones/lista_inscripciones.html', contexto)

def calcular_nota_certificacion(nota_oral, nota_comprension, nota_escritura, nota_lectura):
    """
    Calcula el promedio de las notas de certificación y devuelve el nivel correspondiente.
    Si alguna nota es vacía, se considera como 'BELLOW A1' (valor 1).
    """
    niveles_map = [
        'BELLOW A1', 'A1', 'A1+', 'A2', 'A2+', 'B1', 'B1+', 'B2', 'B2+', 'C1', 'C1+', 'C2'
    ]
    nivel_a_num = {nivel: idx + 1 for idx, nivel in enumerate(niveles_map)}
    num_a_nivel = {idx + 1: nivel for idx, nivel in enumerate(niveles_map)}

    notas = [nota_oral, nota_comprension, nota_escritura, nota_lectura]
    valores = []
    for n in notas:
        if not n or n not in nivel_a_num:
            valores.append(1)  # BELLOW A1
        else:
            valores.append(nivel_a_num[n])
    promedio = round(sum(valores) / 4)
    return num_a_nivel.get(promedio, 'BELLOW A1')

def evaluar_certificacion(request):
    """
    Procesa el formulario del modal para inscripciones de tipo certificación.
    """
    if not request.user.is_authenticated or not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('login')

    filtros = {
        'facultad': request.POST.get('facultad', ''),
        'grupo': request.POST.get('grupo', ''),
        'anio_escolar': request.POST.get('anio_escolar', ''),
        'tipo_convocatoria': request.POST.get('tipo_convocatoria', ''),
        'nivel': request.POST.get('nivel', ''),
    }

    if request.method == "POST":
        inscripcion_id = request.POST.get('inscripcion_id')
        nota_oral = request.POST.get('nota_oral')
        nota_comprension = request.POST.get('nota_comprension')
        nota_escritura = request.POST.get('nota_escritura')
        nota_lectura = request.POST.get('nota_audicion')  # O 'nota_lectura' según tu input

        inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)

        # Solo si la convocatoria es certificación
        if inscripcion.convocatoria.tipo == "certificacion":
            resultado, created = Resultado.objects.get_or_create(inscripcion=inscripcion)
            resultado.notaO = nota_oral
            resultado.notaC = nota_comprension
            resultado.notaE = nota_escritura
            resultado.notaL = nota_lectura
            resultado.nota = calcular_nota_certificacion(nota_oral, nota_comprension, nota_escritura, nota_lectura)
            resultado.save()
            # Actualizar el nivel del usuario al mismo valor que resultado.nota
            usuario = resultado.inscripcion.estudiante
            usuario.nivel = resultado.nota
            usuario.save()
            print("usuario nivel actualizado:", usuario.nivel)
            messages.success(request, "Notas de certificación guardadas correctamente.")
        else:
            messages.error(request, "Esta inscripción no es de tipo certificación.")


        filtros = {
            'facultad': request.POST.get('facultad', ''),
            'grupo': request.POST.get('grupo', ''),
            'anio_escolar': request.POST.get('anio_escolar', ''),
            'tipo_convocatoria': request.POST.get('tipo_convocatoria', ''),
            'nivel': request.POST.get('nivel', ''),
            'buscar': request.POST.get('buscar', ''),
            'filtros_activos': request.POST.get('filtros_activos', ''),
        }

        # Construir la query string
        from urllib.parse import urlencode
        query_string = urlencode({k: v for k, v in filtros.items() if v})
        return redirect(f"{reverse('lista_inscripciones')}?{query_string}")

    # Si no es POST, redirigir a la lista de inscripciones
    return redirect('lista_inscripciones')