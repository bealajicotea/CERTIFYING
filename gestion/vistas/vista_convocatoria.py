from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from gestion.models import Convocatoria
from django.contrib import messages

def lista_convocatorias(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    convocatorias = Convocatoria.objects.all()
    return render(request, 'convocatorias/lista_convocatorias.html', {'convocatorias': convocatorias})

def crear_convocatoria(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')
        lugar = request.POST.get('lugar')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        usuario = request.user

        Convocatoria.objects.create(
            tipo=tipo,
            descripcion=descripcion,
            lugar=lugar,
            fecha=fecha,
            hora=hora,
            usuario=usuario
        )
        messages.success(request, "Convocatoria creada exitosamente.")
        return redirect('lista_convocatorias')

    return render(request, 'convocatorias/crear_convocatoria.html')

def editar_convocatoria(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)

    if request.method == 'POST':
        convocatoria.tipo = request.POST.get('tipo')
        convocatoria.descripcion = request.POST.get('descripcion')
        convocatoria.lugar = request.POST.get('lugar')
        convocatoria.fecha = request.POST.get('fecha')
        convocatoria.hora = request.POST.get('hora')
        convocatoria.save()
        messages.success(request, "Convocatoria editada exitosamente.")
        return redirect('lista_convocatorias')

    return render(request, 'convocatorias/editar_convocatoria.html', {'convocatoria': convocatoria})

def eliminar_convocatoria(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
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
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == "POST":
        ids = request.POST.getlist('convocatorias_seleccionadas')
        if ids:
            Convocatoria.objects.filter(id__in=ids).delete()
            messages.success(request, "Convocatorias eliminadas exitosamente.")
    return redirect('lista_convocatorias')