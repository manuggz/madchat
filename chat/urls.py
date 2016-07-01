from django.conf.urls import url

from . import views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url('^', include('django.contrib.auth.urls')),
    url(r'^enviarMensaje/$', views.enviar_mensaje, name='enviarMensaje'),
    url(r'^recibirActualizaciones/$', views.recibir_actualizaciones, name='recibirActualizaciones'),
]