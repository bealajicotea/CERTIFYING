from apps.usuarios.models import Usuario as User
from django.db import models

class Notification(models.Model):
    verb = models.CharField(max_length=255)  # Qué ocurrió
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, blank=True, related_name="read_notifications")

    def __str__(self):
        return f"Notificación: {self.verb}"