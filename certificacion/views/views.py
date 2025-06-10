from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "¡Bienvenido, {}! Has iniciado sesión correctamente.".format(user.username))
            if user.es_profesor():
                return redirect('pagina_principal')
            return redirect('pagina_principal_e')  # Redirige a la página principal
        else:
            messages.error(request, "Credenciales inválidas. Por favor, verifica tu usuario y contraseña.")
            return redirect('login')  # Redirige al login después de agregar el mensaje de error
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente. ¡Hasta pronto!")
    return redirect('login')  # Redirige al login después de cerrar sesión

def prueba(request):
    return render(request, 'prueba.html')