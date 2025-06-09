"""
URL configuration for certificacion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from certificacion.views import views, student_views, teacher_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.login_view, name='login'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('', include('apps.usuarios.urls')),
    path('', include('apps.resultados.urls')),
    path('', include('apps.inscripciones.urls')),
    path('', include('apps.convocatorias.urls')),
    path('', include('apps.notificaciones.urls')),

    path('pagina_principal/', teacher_views.index_view, name='pagina_principal'),
    path('pagina_principal_e/', student_views.index_view_e, name='pagina_principal_e'),

    path('prueba/', views.prueba, name='prueba'),

    path('descargar-certificado/', student_views.generar_certificado, name='descargar_certificado'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





