from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# 15Ma_Nu1 2chu toston cotufa caramelada


class Mensaje(models.Model):
    mensaje_contenido = models.TextField()
    usuario_creador = models.ForeignKey(User)
