# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.notificaciones.models import Notification
from apps.convocatorias.models import Convocatoria  # tu modelo objetivo

@receiver(post_save, sender=Convocatoria)
def notificar_nueva_convocatoria(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            verb=f"Se ha creado una nueva :{instance.tipo}",
            url=f"/convocaorias_e/detalle/{instance.id}/"
        )
