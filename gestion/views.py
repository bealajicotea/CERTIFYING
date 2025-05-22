from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.es_profesor():
                return redirect('pagina_principal')
            return redirect('pagina_principal_e')  # Redirige a la página principal
        else:
            # Renderiza la página con un mensaje de error
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión


def index_view(request):
    return render(request, 'pagina_principal.html')

def index_view_e(request):
    return render(request, 'rol_estudiante/pagina_principal_e.html')

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

def prueba(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    return render(request, 'prueba.html')