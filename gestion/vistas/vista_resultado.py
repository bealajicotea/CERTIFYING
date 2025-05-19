from django.shortcuts import render, redirect, get_object_or_404
from gestion.models import Resultado, Inscripcion
from gestion.forms import ResultadoForm
from django.contrib import messages

def lista_resultados(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    resultados = Resultado.objects.all()
    return render(request, 'resultados/lista_resultados.html', {'resultados': resultados})

def crear_resultado(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == 'POST':
        form = ResultadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_resultados')
    else:
        form = ResultadoForm()
    return render(request, 'resultados/crear_resultado.html', {'form': form})

def eliminar_resultado(request, resultado_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    resultado = get_object_or_404(Resultado, id=resultado_id)
    resultado.delete()
    return redirect('lista_resultados')

def eliminar_resultados_seleccionados(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    if request.method == "POST":
        ids = request.POST.getlist('resultados_seleccionados')
        if ids:
            Resultado.objects.filter(id__in=ids).delete()
    return redirect('lista_resultados')

def editar_resultado(request, resultado_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    if not request.user.es_profesor():
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('pagina_principal')

    resultado = get_object_or_404(Resultado, id=resultado_id)
    if request.method == 'POST':
        form = ResultadoForm(request.POST, instance=resultado)
        if form.is_valid():
            form.save()
            return redirect('lista_resultados')
    else:
        form = ResultadoForm(instance=resultado)
    return render(request, 'resultados/editar_resultado.html', {'form': form})

def detalle_resultado(request, resultado_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    resultado = get_object_or_404(Resultado, id=resultado_id)
    return render(request, 'resultados/detalle_resultado.html', {'resultado': resultado})

