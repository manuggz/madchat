from channels.routing import route

from chat.consumers import ws_message, ws_add, ws_disconnect, msg_consumer

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    route("chat-messages", msg_consumer),
]
