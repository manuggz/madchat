from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# 15Ma_Nu1 2chu toston cotufa caramelada

class Mensaje(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class MensajeUsuario(models.Model):
    mensaje_contenido = models.CharField(max_length=200)
    usuario_creador = models.ForeignKey(User)


class MensajeConectadoChat(models.Model):
    usuario = models.ForeignKey(User)
