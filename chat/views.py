from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ChatUser


@login_required
def index(request):

    context = {}

    # Nota: Excluimos al usuario actual(.exclude) para que se agregue a la
    # lista de conectados(chat/index.html[#lista-conectados]) cuando se llame a consumers.ws_add[linea 52 : Group.send]
    # para que no se agregue dos veces(Cuando se carga y cuando se conecta)
    context['conectados'] = ChatUser.objects.filter(n_conecciones__gt=0).exclude(user=request.user)
    return render(request, 'chat/index.html', context)
