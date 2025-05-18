from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from gestion.models import Inscripcion, Usuario
from django.contrib import messages

def lista_inscripciones(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    inscripciones = Inscripcion.objects.all()
    return render(request, 'inscripciones/lista_inscripciones.html', {'inscripciones': inscripciones})

def crear_inscripcion(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante')
        tipo_examen = request.POST.get('tipo_examen')

        estudiante = Usuario.objects.get(id=estudiante_id)
        Inscripcion.objects.create(estudiante=estudiante, tipo_examen=tipo_examen)
        return redirect('lista_inscripciones')

    estudiantes = Usuario.objects.filter(tipo_usuario='estudiante')
    return render(request, 'inscripciones/crear_inscripcion.html', {'estudiantes': estudiantes})

def eliminar_inscripcion(request, inscripcion_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    inscripcion.delete()
    return redirect('lista_inscripciones')

def eliminar_inscripciones_seleccionadas(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    if request.method == "POST":
        ids = request.POST.getlist('inscripciones_seleccionadas')
        if ids:
            Inscripcion.objects.filter(id__in=ids).delete()
    return redirect('lista_inscripciones')

def editar_inscripcion(request, inscripcion_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante')
        tipo_examen = request.POST.get('tipo_examen')
        if estudiante_id:
            inscripcion.estudiante = Usuario.objects.get(id=estudiante_id)
        if tipo_examen:
            inscripcion.tipo_examen = tipo_examen
        inscripcion.save()
        return redirect('lista_inscripciones')
    estudiantes = Usuario.objects.filter(tipo_usuario='estudiante')
    return render(request, 'inscripciones/editar_inscripcion.html', {'inscripcion': inscripcion, 'estudiantes': estudiantes})