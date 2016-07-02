import json

from channels import Channel
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.contrib.auth.models import User

from chat.models import  Mensaje


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
            usuario_creador=User.objects.get(username=message.content['username']),
            mensaje_contenido=message.content['mensaje'],
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
    Group("chat").add(message.reply_channel)

    Group("chat").send({'text': json.dumps({
        'tipo_mensaje': 'conectado_chat',
        'username': message.user.username
    })
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
