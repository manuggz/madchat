from django.contrib import admin

# Register your models here.
from .models import MensajeInicioSesion,MensajeUsuario,Mensaje

admin.site.register(MensajeUsuario)
admin.site.register(MensajeInicioSesion)
admin.site.register(Mensaje)

