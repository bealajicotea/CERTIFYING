from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from gestion.models import Usuario

def verificar_profesor(user):
    return user.es_profesor()

@login_required

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(verificar_profesor)
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

@login_required
@user_passes_test(verificar_profesor)
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

@login_required
@user_passes_test(verificar_profesor)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')