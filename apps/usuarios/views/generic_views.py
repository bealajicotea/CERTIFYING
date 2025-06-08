from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from apps.usuarios.forms import UsuarioForm

def editar_perfil(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')

    usuario = request.user
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            # Si el usuario cambió la contraseña, actualizarla correctamente
            password = form.cleaned_data.get('password')
            if password and password != usuario.password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # Mantiene la sesión activa tras cambiar contraseña
            else:
                user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_perfil.html', {'form': form})

def perfil(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    
    return render(request, 'perfil.html')

def foto(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    return render(request, 'foto.html')

