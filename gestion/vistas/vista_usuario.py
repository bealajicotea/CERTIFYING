from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from gestion.models import Usuario
from gestion.forms import UsuarioForm
from django.contrib import messages

def lista_usuarios(request): 
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

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
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


def editar_usuario(request, usuario_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            # No cambiar contraseña aquí a menos que se provea una nueva
            usuario.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})


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