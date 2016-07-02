from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import MensajeUsuario, MensajeInicioSesion,  Mensaje


@login_required
def index(request):

    contexto = {}

    try:
        mostrado_inisesion = request.session['mostrado_mensaje_inisesion']
    except KeyError:
        mostrado_inisesion = False

    if not mostrado_inisesion:

        # Creamos el mensaje de inicio de sesion
        nuevo_mensaje = MensajeInicioSesion(usuario=request.user)
        nuevo_mensaje.save()

        # Guardamos el mensaje de inicio de sesion , para que se muestre
        m = Mensaje(content_object=nuevo_mensaje)
        m.save()

        request.session['mostrado_mensaje_inisesion'] = True

        # Guardamos el ultimo mensaje de la base de datos para comenzar a mandar
        # al usuario los que les sigan
        request.session['ultimo_actualizado'] = m.pk - 1

    return render(request, 'chat/index.html', contexto)


@login_required
def enviar_mensaje(request):

    if request.method == 'POST':

        msg = request.POST.get('mensaje')

        # Creamos el mensaje
        nuevo_mensaje = MensajeUsuario(mensaje_contenido=msg, usuario_creador=request.user)
        nuevo_mensaje.save()

        # Guardamos el mensaje, para que se muestre
        m = Mensaje(content_object=nuevo_mensaje)
        m.save()

        # Decimos hey! ok -- Actualmente se envia el mensaje de nuevo para que se muestre en pantalla
        return JsonResponse({'username': request.user.username, 'mensaje': msg})
    else:
        return HttpResponse("Método no permitido.", content_type="text/plain", status=405)  # 405 Method Not Allowed


# Metodo inseguro - cualquiera puede ver
@login_required
def recibir_actualizaciones(request):

    if request.method == 'GET':
        # Obtenemos los mensajes que no ha leido el usuario

        mensajes_no_leidos = Mensaje.objects.filter(pk__gt=request.session['ultimo_actualizado'])

        no_leidos = []

        if mensajes_no_leidos.exists():

            # Parseamos los no leidos
            for no_leido in mensajes_no_leidos:

                mensaje = no_leido.content_object

                if no_leido.content_type == ContentType.objects.get_for_model(MensajeUsuario):
                    mensaje_no_leido_dict = {
                        'tipo': 'mensaje_usuario',
                        'username': mensaje.usuario_creador.username,
                        'mensaje': mensaje.mensaje_contenido
                    }

                    #if mensaje.usuario_creador.pk != request.user.pk:  # Si no es uno que envio el usuario actual
                    no_leidos.append(mensaje_no_leido_dict)

                elif no_leido.content_type == ContentType.objects.get_for_model(MensajeInicioSesion):
                    mensaje_no_leido_dict = {
                        'tipo': 'mensaje_inicio_sesion',
                        'username': mensaje.usuario.username
                    }
                    no_leidos.append(mensaje_no_leido_dict)

            # Actualizamos el ultimo leido
            request.session['ultimo_actualizado'] = Mensaje.objects.order_by('-pk')[0].pk

        return JsonResponse({'mensajes': no_leidos})
    else:
        return HttpResponse("Método no permitido.", content_type="text/plain", status=405)  # 405 Method Not Allowed
