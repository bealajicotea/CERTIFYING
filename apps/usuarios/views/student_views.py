from django.shortcuts import render, redirect
from django.contrib import messages


def perfil_e(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    
    return render(request, 'rol_estudiante/perfil_e.html')
