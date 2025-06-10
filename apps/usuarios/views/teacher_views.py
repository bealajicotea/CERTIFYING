from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from apps.usuarios.models import Usuario
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

# --- Funciones auxiliares de filtrado y búsqueda para Usuario ---

def filtrar_usuarios(filtros):
    """
    Filtra usuarios por campos exactos.
    Si todos los filtros están vacíos, retorna todos los usuarios.
    """
    usuarios = Usuario.objects.all()

    facultad = filtros.get('facultad', '')
    grupo = filtros.get('grupo', '')
    anio_escolar = filtros.get('anio_escolar', '')
    carrera = filtros.get('carrera', '')
    tipo_usuario = filtros.get('tipo_usuario', '')

    # Los filtros deben ser exactos, no icontains, porque son choices
    if facultad:
        usuarios = usuarios.filter(facultad=facultad)
    if grupo:
        usuarios = usuarios.filter(grupo=grupo)
    if anio_escolar:
        usuarios = usuarios.filter(anio_escolar=anio_escolar)
    if carrera:
        usuarios = usuarios.filter(carrera=carrera)
    if tipo_usuario:
        usuarios = usuarios.filter(tipo_usuario=tipo_usuario)

    return usuarios

def buscar_en_usuarios(usuarios, buscar):
    """
    Busca en los usuarios filtrados por varios campos.
    """
    if buscar:
        return usuarios.filter(
            Q(username__icontains=buscar) |
            Q(first_name__icontains=buscar) |
            Q(last_name__icontains=buscar) |
            Q(email__icontains=buscar) |
            Q(facultad__icontains=buscar) |
            Q(grupo__icontains=buscar) |
            Q(anio_escolar__icontains=buscar) |
            Q(carrera__icontains=buscar) |
            Q(tipo_usuario__icontains=buscar)
        )
    return usuarios

def obtener_usuarios_filtrados(filtros):
    """
    Aplica primero el filtrado y luego la búsqueda.
    """
    usuarios = filtrar_usuarios(filtros)
    buscar = filtros.get('buscar', '')
    usuarios = buscar_en_usuarios(usuarios, buscar)

    facultades = Usuario.fac
    grupos = Usuario.group
    anios = Usuario.anios
    carreras = Usuario.car
    tipos_usuario = Usuario.TIPO_USUARIO

    contexto = {
        'usuarios': usuarios,
        'facultades': facultades,
        'grupos': grupos,
        'anios': anios,
        'carreras': carreras,
        'tipos_usuario': tipos_usuario,
        'selected_facultad': filtros.get('facultad', ''),
        'selected_grupo': filtros.get('grupo', ''),
        'selected_anio': filtros.get('anio_escolar', ''),
        'selected_carrera': filtros.get('carrera', ''),
        'selected_tipo_usuario': filtros.get('tipo_usuario', ''),
        'buscar': buscar,
        'filtros_activos': filtros.get('filtros_activos', ''),
    }
    return contexto

def lista_usuarios(request):
    # Asegúrate de que los parámetros GET se pasen correctamente
    filtros = {
        'facultad': request.GET.get('facultad', ''),
        'grupo': request.GET.get('grupo', ''),
        'anio_escolar': request.GET.get('anio_escolar', ''),
        'carrera': request.GET.get('carrera', ''),
        'tipo_usuario': request.GET.get('tipo_usuario', ''),
        'buscar': request.GET.get('buscar', ''),
        'filtros_activos': request.GET.get('filtros_activos', ''),
    }
    contexto = obtener_usuarios_filtrados(filtros)
    # Paginación
    usuarios = contexto['usuarios']
    page_number = request.GET.get('page', 1)
    paginator = Paginator(usuarios, 6)  # 10 por página
    page_obj = paginator.get_page(page_number)
    contexto['usuarios'] = page_obj
    contexto['page_obj'] = page_obj
    contexto['is_paginated'] = page_obj.has_other_pages()
    return render(request, 'usuarios/lista_usuarios.html', contexto)


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
        messages.success(request, "Usuario creado correctamente.")
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