from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from gestion.models import Resultado, Usuario

def lista_resultados(request):
    resultados = Resultado.objects.all()
    return render(request, 'resultados/lista_resultados.html', {'resultados': resultados})


def crear_resultado(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante')
        tipo_examen = request.POST.get('tipo_examen')
        nivel = request.POST.get('nivel')

        estudiante = Usuario.objects.get(id=estudiante_id)
        Resultado.objects.create(estudiante=estudiante, tipo_examen=tipo_examen, nivel=nivel)
        return redirect('lista_resultados')

    estudiantes = Usuario.objects.filter(tipo_usuario='estudiante')
    return render(request, 'resultados/crear_resultado.html', {'estudiantes': estudiantes})


def eliminar_resultado(request, resultado_id):
    resultado = get_object_or_404(Resultado, id=resultado_id)
    resultado.delete()
    return redirect('lista_resultados')


def eliminar_resultados_seleccionados(request):
    if request.method == "POST":
        ids = request.POST.getlist('resultados_seleccionados')
        if ids:
            Resultado.objects.filter(id__in=ids).delete()
    return redirect('lista_resultados')


def editar_resultado(request, resultado_id):
    resultado = get_object_or_404(Resultado, id=resultado_id)
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante')
        tipo_examen = request.POST.get('tipo_examen')
        nivel = request.POST.get('nivel')
        if estudiante_id:
            resultado.estudiante = Usuario.objects.get(id=estudiante_id)
        if tipo_examen:
            resultado.tipo_examen = tipo_examen
        if nivel:
            resultado.nivel = nivel
        resultado.save()
        return redirect('lista_resultados')
    estudiantes = Usuario.objects.filter(tipo_usuario='estudiante')
    return render(request, 'resultados/editar_resultado.html', {'resultado': resultado, 'estudiantes': estudiantes})