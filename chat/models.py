from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#15Ma_Nu1 2chu toston

class Mensaje(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

class MensajeUsuario(models.Model):
    mensaje_contenido = models.CharField(max_length=200)
    usuario_creador   = models.ForeignKey('Usuario')

class MensajeInicioSesion(models.Model):
    usuario = models.ForeignKey('Usuario')


class Usuario(models.Model):
	username = models.CharField(max_length=100,primary_key=True)