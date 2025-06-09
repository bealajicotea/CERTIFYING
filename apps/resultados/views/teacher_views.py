from django.shortcuts import render, redirect, get_object_or_404
from apps.resultados.models import Resultado
from apps.inscripciones.models import Inscripcion
from apps.usuarios.models import Usuario
from django.contrib import messages

def lista_resultados(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    resultados = Resultado.objects.all()
    return render(request, 'resultados/lista_resultados.html', {'resultados': resultados})

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
            messages.error(request, "¡Ya existe un resultado para esta inscripción (estudiante y convocatoria)!")
        else:
            resultado = Resultado(
                inscripcion_id=inscripcion_id,
                nota=nivel
            )
            resultado.save()
            messages.success(request, "Resultado creado exitosamente.")
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
        messages.success(request, "Resultado editado exitosamente.")
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
