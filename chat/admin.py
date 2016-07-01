from django.contrib import admin

# Register your models here.
from .models import Usuario,MensajeInicioSesion,MensajeUsuario,Mensaje

admin.site.register(Usuario)
admin.site.register(MensajeUsuario)
admin.site.register(MensajeInicioSesion)
admin.site.register(Mensaje)

