from django.contrib import admin

# Register your models here.
from .models import Mensaje,ChatUser

admin.site.register(Mensaje)
admin.site.register(ChatUser)


