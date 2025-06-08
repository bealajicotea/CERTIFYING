# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.notificaciones.models import Notification

@login_required
def notificaciones(request):
    todas = Notification.objects.all()
    no_leidas = todas.exclude(read_by=request.user)
    return render(request, "lista_notificaciones.html", {
        "no_leidas": no_leidas,
        "todas": todas,
    })

@login_required
def marcar_como_leida(request, pk):
    noti = Notification.objects.get(pk=pk)
    noti.read_by.add(request.user)
    return redirect(noti.url or "/")
