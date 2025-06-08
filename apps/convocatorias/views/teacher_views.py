from django.shortcuts import render, redirect, get_object_or_404
from apps.convocatorias.models import Convocatoria
from apps.notificaciones.models import Notification
from apps.inscripciones.models import Inscripcion
from apps.usuarios.models import Usuario
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
    return render(request, 'convocatorias/crear_convocatoria.html')

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
    return render(request, 'convocatorias/editar_convocatoria.html', {'convocatoria': convocatoria})

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