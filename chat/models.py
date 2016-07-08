from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# 15Ma_Nu1 2chupetas de 50 toston 170 cotufa 120 caramelada tostonnuevo 180 chees tres 180
# dos chupis


class Mensaje(models.Model):
    mensaje_contenido = models.TextField()
    usuario_creador = models.ForeignKey(User)

    def __str__(self):
        return self.mensaje_contenido


class ChatUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    n_conecciones = models.IntegerField(default=0)

    def esta_conectado(self):
        return self.n_conecciones > 0

    def agregar_coneccion(self):
        self.n_conecciones+=1
        self.save()

    def eliminar_coneccion(self):
        self.n_conecciones-=1
        if self.n_conecciones < 0: self.n_conecciones = 0
        self.save()

    def __str__(self):
        return self.user.username