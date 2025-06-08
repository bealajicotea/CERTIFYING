from django.shortcuts import render, redirect, get_object_or_404
from apps.convocatorias.models import Convocatoria
from apps.inscripciones.models import Inscripcion
from apps.usuarios.models import Usuario
from apps.convocatorias.forms import ConvocatoriaForm
from django.contrib import messages

def lista_convocatorias(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    convocatorias = Convocatoria.objects.all()
    return render(request, 'convocatorias/lista_convocatorias.html', {'convocatorias': convocatorias})

def crear_convocatoria(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == 'POST':
        form = ConvocatoriaForm(request.POST)
        if form.is_valid():
            convocatoria = form.save(commit=False)
            convocatoria.profesor = request.user
            convocatoria.save()
            # maria mmmmmmmm
            # Inscribir automáticamente estudiantes de primer año si es de tipo colocacion
            if convocatoria.tipo == 'colocacion':
                print("Convocatoria de colocación")
                estudiantes = Usuario.objects.filter(tipo_usuario='estudiante', anio_escolar='1')
                inscripciones = [
                    Inscripcion(estudiante=est, convocatoria=convocatoria)
                    for est in estudiantes
                ]
                Inscripcion.objects.bulk_create(inscripciones)
            messages.success(request, "Convocatoria creada exitosamente.")
            return redirect('lista_convocatorias')
    else:
        form = ConvocatoriaForm()
    return render(request, 'convocatorias/crear_convocatoria.html', {'form': form})

def editar_convocatoria(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    if request.method == 'POST':
        form = ConvocatoriaForm(request.POST, instance=convocatoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Convocatoria editada exitosamente.")
            return redirect('lista_convocatorias')
    else:
        form = ConvocatoriaForm(instance=convocatoria)
    return render(request, 'convocatorias/editar_convocatoria.html', {'form': form})

def eliminar_convocatoria(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    convocatoria.delete()
    messages.success(request, "Convocatoria eliminada exitosamente.")
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
    return redirect('lista_convocatorias')

def detalle_convocatoria(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    return render(request, 'convocatorias/detalle_convocatoria.html', {'convocatoria': convocatoria})