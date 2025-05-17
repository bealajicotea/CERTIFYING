from django.contrib import admin
from .models import Usuario, Convocatoria, Resultado, Inscripcion

admin.site.register(Usuario)
admin.site.register(Convocatoria)
admin.site.register(Resultado)
admin.site.register(Inscripcion)

