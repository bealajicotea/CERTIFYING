from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from gestion.models import Usuario
from django.contrib import messages

def lista_usuarios(request): 
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def crear_usuario(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == 'POST':
        username = request.POST.get('username')
        correo_uci = request.POST.get('correo_uci')
        nombre = request.POST.get('nombre')
        tipo_usuario = request.POST.get('tipo_usuario')
        password = request.POST.get('password')
        facultad = request.POST.get('facultad')
        grupo = request.POST.get('grupo')
        anio_escolar = request.POST.get('anio_escolar')
        carrera = request.POST.get('carrera')
        curso = request.POST.get('curso')
        nivel = request.POST.get('nivel')

        nuevo_usuario = Usuario(
            username=username,
            email=correo_uci,
            first_name=nombre,
            tipo_usuario=tipo_usuario,
            facultad=facultad,
            grupo=grupo,
            anio_escolar=anio_escolar,
            carrera=carrera,
            curso=curso,
            nivel=nivel,
            password=make_password(password)
        )
        nuevo_usuario.save()
        return redirect('lista_usuarios')

    return render(request, 'usuarios/crear_usuario.html')


def editar_usuario(request, usuario_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('correo_uci')
        usuario.first_name = request.POST.get('nombre')
        usuario.tipo_usuario = request.POST.get('tipo_usuario')
        usuario.facultad = request.POST.get('facultad')
        usuario.grupo = request.POST.get('grupo')
        usuario.anio_escolar = request.POST.get('anio_escolar')
        usuario.carrera = request.POST.get('carrera')
        usuario.curso = request.POST.get('curso')
        usuario.nivel = request.POST.get('nivel')
        usuario.save()
        return redirect('lista_usuarios')

    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})


def eliminar_usuario(request, usuario_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')


def eliminar_usuarios_seleccionados(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not es_profesor(request.user):
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == "POST":
        ids = request.POST.getlist('usuarios_seleccionados')
        if ids:
            Usuario.objects.filter(id__in=ids).delete()
            messages.success(request, "Usuarios eliminados correctamente.")
        else:
            messages.warning(request, "No se seleccionó ningún usuario.")
    return redirect('lista_usuarios')