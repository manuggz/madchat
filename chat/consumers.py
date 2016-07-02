import json

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    data = json.loads(message['text'])

    mensaje_push = {
        'username': message.user.username,
        'mensaje': data['mensaje']
    }

    Group("chat").send({'text': json.dumps(mensaje_push)})


# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    Group("chat").add(message.reply_channel)


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
