from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

def editar_perfil(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')

    usuario = request.user
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
        if password and password != usuario.password:
            usuario.set_password(password)
            usuario.save()
            update_session_auth_hash(request, usuario)
        else:
            usuario.save()
        if files.get('foto_perfil'):
            usuario.foto_perfil = files.get('foto_perfil')
            usuario.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')
    return render(request, 'editar_perfil.html', {'usuario': usuario})

def perfil(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not hasattr(request.user, 'es_profesor') or not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta página.")
        return redirect('pagina_principal')
    return render(request, 'perfil.html')

def foto(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    return render(request, 'foto.html')

