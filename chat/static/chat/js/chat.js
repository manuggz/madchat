// Note that the path doesn't matter right now; any WebSocket
// connection gets bumped over to WebSocket consumers

socket = new WebSocket("ws://" + window.location.host + "/chat/");

socket.onmessage = function (message) {

    var data = JSON.parse(message.data);
    var chat = $('#chat-txtboard');

    if (data.tipo_mensaje == "broadcast") {
        chat.append(crear_mensaje_html(data.username, data.mensaje));
    } else if (data.tipo_mensaje == "conectado_chat") {
        chat.append(crear_mensaje_conectado_html(data.username));
    }

    //Movemos el chat al ultimo elemento enviado - recibido(esperemos sea este)
    chat.scrollTop(chat.prop("scrollHeight"));
};


$(document).ready(function(){


    $('#form-mensaje').on('submit', function (event) {

        var inpTxtMensaje = $('#inpTxtMensaje');
        var texto_enviar = inpTxtMensaje.val();

	    event.preventDefault();

        if(texto_enviar){
            if(texto_enviar.trim().length > 0){
                socket.send(
                    JSON.stringify({
                        'mensaje': inpTxtMensaje.val()
                    })
                );
            }

            inpTxtMensaje.val('').focus(); // remove the value from the input

        }
        return false;
        
	});

    var chat_txtboard = $('#chat-txtboard');
    chat_txtboard.scrollTop(chat_txtboard.prop("scrollHeight"));


});


function crear_mensaje_html(username,mensaje){
    return '<div><span class="glyphicon glyphicon-user" aria-hidden="true"></span><b> ' + username + ': </b>' + 
                    mensaje + '</div>'
}

function crear_mensaje_conectado_html(username){
    return '<div><span class="glyphicon glyphicon-user" aria-hidden="true"></span><b> '
        + username +
        ' se ha conectado al chat. </b></div>'
}

