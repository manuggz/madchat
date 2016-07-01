from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^enviarMensaje/$', views.enviarMensaje, name='enviarMensaje'),
    url(r'^recibirActualizaciones/$', views.recibirActualizaciones, name='recibirActualizaciones'),
]