from django.contrib import admin

# Register your models here.
from .models import MensajeConectadoChat, MensajeUsuario, Mensaje

admin.site.register(MensajeUsuario)
admin.site.register(MensajeConectadoChat)
admin.site.register(Mensaje)

