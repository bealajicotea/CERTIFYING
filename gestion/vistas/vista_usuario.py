from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from gestion.models import Usuario
from django.contrib import messages


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        correo_uci = request.POST.get('correo_uci')
        nombre = request.POST.get('nombre')
        tipo_usuario = request.POST.get('tipo_usuario')
        password = request.POST.get('password')

        nuevo_usuario = Usuario(
            username=username,
            email=correo_uci,
            first_name=nombre,
            tipo_usuario=tipo_usuario,
            password=make_password(password)
        )
        nuevo_usuario.save()
        return redirect('lista_usuarios')

    return render(request, 'usuarios/crear_usuario.html')


def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('correo_uci')
        usuario.first_name = request.POST.get('nombre')
        usuario.tipo_usuario = request.POST.get('tipo_usuario')
        usuario.save()
        return redirect('lista_usuarios')

    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')

def eliminar_usuarios_seleccionados(request):
    if request.method == "POST":
        ids = request.POST.getlist('usuarios_seleccionados')
        if ids:
            User.objects.filter(id__in=ids).delete()
            messages.success(request, "Usuarios eliminados correctamente.")
        else:
            messages.warning(request, "No se seleccionó ningún usuario.")
    return redirect('lista_usuarios')