import json
from channels import Channel
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.contrib.auth.models import User

from chat.models import  Mensaje, ChatUser


# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    data = json.loads(message['text'])

    # Stick the message onto the processing queue
    Channel("chat-messages").send({
        'tipo_mensaje': 'broadcast',
        'username': message.user.username,
        "mensaje": data['mensaje'],
    })


# Connected to chat-messages
def msg_consumer(message):

    mensaje_push = {}

    if message.content['tipo_mensaje'] == 'broadcast':

        Mensaje.objects.create(
            usuario_creador   = User.objects.get(username=message.content['username']),
            mensaje_contenido = message.content['mensaje'],
        )

        mensaje_push = {
            'tipo_mensaje': 'broadcast',
            'username': message.content['username'],
            'mensaje': message.content['mensaje'],
        }

    Group("chat").send({'text': json.dumps(mensaje_push)})


# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):

    chat_user, is_created = ChatUser.objects.get_or_create(user=message.user)

    Group("chat").add(message.reply_channel)

    if not chat_user.esta_conectado(): #Avisamos a todos los usuarios conectados
        Group("chat").send({'text': json.dumps({
            'tipo_mensaje': 'conectado_chat',
            'username': message.user.username
        })
        })

    chat_user.agregar_coneccion()

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):

    Group("chat").discard(message.reply_channel)

    chat_user = ChatUser.objects.get(user=message.user)
    chat_user.eliminar_coneccion()

    if not chat_user.esta_conectado():  # Avisamos a todos los usuarios conectados
        Group("chat").send({'text': json.dumps({
            'tipo_mensaje': 'desconectado_chat',
            'username': message.user.username
        })
        })
