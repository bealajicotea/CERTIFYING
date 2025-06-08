from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def perfil_estudiante(request):
    if not hasattr(request.user, 'es_estudiante') or not request.user.es_estudiante():
      messages.warning(request, "No tienes permisos para acceder a esta página.")
    return render(request, 'rol_estudiante/perfil_e.html')


@login_required
def editar_perfil_e(request):
    usuario = request.user
    if not hasattr(usuario, 'es_estudiante') or not usuario.es_estudiante():
        messages.warning(request, "No tienes permisos para acceder a esta página.")
        return redirect('pagina_principal_e')

    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.carrera = request.POST.get('carrera', usuario.carrera)
        usuario.grupo = request.POST.get('grupo', usuario.grupo)
        usuario.facultad = request.POST.get('facultad', usuario.facultad)
        usuario.anio_escolar = request.POST.get('anio_escolar', usuario.anio_escolar)
        usuario.curso = request.POST.get('curso', usuario.curso)
        usuario.nivel = request.POST.get('nivel', usuario.nivel)
        usuario.tipo_usuario = "estudiante"

        if request.FILES.get('foto_perfil'):
            usuario.foto_perfil = request.FILES['foto_perfil']

        usuario.save()
        messages.success(request, "Perfil actualizado correctamente.")
        # Redirigir al perfil del estudiante
        return redirect('perfil_estudiante')

    return render(request, 'rol_estudiante/editar_perfil_e.html', {'usuario': usuario})