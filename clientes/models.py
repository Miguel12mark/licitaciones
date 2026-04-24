from django.db import models
from django.conf import settings


class Cliente(models.Model):
    nombre = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="clientes_creados"
    )

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.nombre