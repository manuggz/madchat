from django.shortcuts import render
from django.http import HttpResponse
from .models import MensajeUsuario,MensajeInicioSesion,Usuario,Mensaje
from random import randint
from django.contrib.contenttypes.models import ContentType

def index(request):

	contexto = {}

	if request.session.get('username') is None: # Si es un nevo usuario

		##Creamos un nombre de usuario aleatorio
		request.session['username'] = 'Anonimo' + str(randint(0,10000))

		usuarioActual = Usuario(username=request.session['username'])
		usuarioActual.save()

		#Creamos el mensaje de inicio de sesion
		nuevoMensaje = MensajeInicioSesion(usuario=usuarioActual)
		nuevoMensaje.save()

		#Guardamos el mensaje de inicio de sesion , para que se muestre
		m = Mensaje(content_object=nuevoMensaje)
		m.save()


	#Guardamos el ultimo mensaje de la base de datos para comenzar a mandar
	#al usuario los que les sigan
	try:
		request.session['ultimo_actualizado'] =  Mensaje.objects.order_by('-pk')[0].pk
	except IndexError: # Ups! no hay mensajes 
		request.session['ultimo_actualizado'] = -1

	contexto['username'] = request.session['username']
	return render(request, 'chat/index.html', contexto)


def enviarMensaje(request):

	usuarioActual = Usuario.objects.get(pk=request.session['username'])

	if request.method == 'POST':

		msg = request.POST.get('mensaje')

		#Creamos el mensaje
		nuevoMensaje = MensajeUsuario(mensaje_contenido=msg,usuario_creador=usuarioActual)
		nuevoMensaje.save()

		#Guardamos el mensaje, para que se muestre
		m = Mensaje(content_object=nuevoMensaje)
		m.save()

		#Decimos hey! ok -- Actualmente se envia el mensaje de nuevo para que se muestre en pantalla
		return JsonResponse({'username':usuarioActual.username,'mensaje':msg})
	else:
		return HttpResponse("Método no permitido.", content_type="text/plain",status=405) # 405 Method Not Allowed

#Metodo inseguro - cualquiera puede ver
def recibirActualizaciones(request):

	if request.method == 'GET':
		#Obtenemos los mensajes que no ha leido el usuario

		mensajes_no_leidos = Mensaje.objects.filter(pk__gt = request.session['ultimo_actualizado'])

		no_leidos = [] 

		if mensajes_no_leidos.exists():

			#Obtenemos el objeto usuario actual
			usuarioActual = Usuario.objects.get(pk=request.session['username'])

			#Parseamos los no leidos
			for no_leido in mensajes_no_leidos:

				mensaje = no_leido.content_object
				mensaje_no_leido_dict = {}

				if no_leido.content_type == ContentType.objects.get_for_model(MensajeUsuario):
					mensaje_no_leido_dict = {
					'tipo':'mensaje_usuario',
					'username':mensaje.usuario_creador.username,
					'mensaje':mensaje.mensaje_contenido
					}

					if mensaje.usuario_creador.pk != usuarioActual.pk: #Si no es uno que envio el usuario actual
						no_leidos.append(mensaje_no_leido_dict)

				elif no_leido.content_type == ContentType.objects.get_for_model(MensajeInicioSesion):
					mensaje_no_leido_dict = {
					'tipo':'mensaje_inicio_sesion',
					'username':mensaje.usuario.username
					}
					no_leidos.append(mensaje_no_leido_dict)

			#Actualizamos el ultimo leido
			request.session['ultimo_actualizado'] = Mensaje.objects.order_by('-pk')[0].pk


		return JsonResponse({'mensajes':no_leidos})
	else:
		return HttpResponse("Método no permitido.", content_type="text/plain",status=405) # 405 Method Not Allowed
