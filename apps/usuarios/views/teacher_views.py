from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from apps.usuarios.models import Usuario
from django.contrib import messages

def lista_usuarios(request): 
    

    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def crear_usuario(request):
    '''if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')'''

    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        usuario = Usuario(
            username=data.get('username'),
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            tipo_usuario=data.get('tipo_usuario'),
            facultad=data.get('facultad') or None,
            anio_escolar=data.get('anio_escolar') or None,
            grupo=data.get('grupo') or '',
            carrera=data.get('carrera') or None,
            curso=data.get('curso') or None,
            nivel=data.get('nivel') or None,
        )
        password = data.get('password')
        if password:
            usuario.password = make_password(password)
        if files.get('foto_perfil'):
            usuario.foto_perfil = files.get('foto_perfil')
        usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/crear_usuario.html')

def editar_usuario(request, usuario_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        usuario.username = data.get('username')
        usuario.email = data.get('email')
        usuario.first_name = data.get('first_name')
        usuario.last_name = data.get('last_name')
        usuario.tipo_usuario = data.get('tipo_usuario')
        usuario.facultad = data.get('facultad') or None
        usuario.anio_escolar = data.get('anio_escolar') or None
        usuario.grupo = data.get('grupo') or ''
        usuario.carrera = data.get('carrera') or None
        usuario.curso = data.get('curso') or None
        usuario.nivel = data.get('nivel') or None
        password = data.get('password')
        if password:
            usuario.password = make_password(password)
        if files.get('foto_perfil'):
            usuario.foto_perfil = files.get('foto_perfil')
        usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})


def eliminar_usuario(request, usuario_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')


def eliminar_usuarios_seleccionados(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
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

def detalle_usuario(request, usuario_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'usuarios/detalle_usuario.html', {'usuario': usuario})