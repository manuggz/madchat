// Note that the path doesn't matter right now; any WebSocket
// connection gets bumped over to WebSocket consumers

socket = new WebSocket("ws://" + window.location.host + "/chat/");

socket.onmessage = function (message) {

    var data = JSON.parse(message.data);
    var chat = $('#chat');
    if (data.tipo_mensaje == "broadcast") {
        chat.append($(crear_mensaje_html(data.username, data.mensaje)).hide().fadeIn(200));
    }else if(data.tipo_mensaje == "conectado_chat") {
        //chat.append(crear_mensaje_conectado_html(data.username));
    }else if(data.tipo_mensaje == "desconectado_chat"){
        //chat.append(crear_mensaje_desconectado_html(data.username));
    }

    if($('#username').val() == data.username){ //Si es un mensaje enviado por el mismo movemos el scroll para abajo
        //Movemos el chat al ultimo elemento enviado - recibido(esperemos sea este)
        $("html, body").animate({ scrollTop: $(document).height()-$(window).height() },200);
    }
};


$(document).ready(function(){

    $('#text-mensaje').keyup(function(e){
        if(e.keyCode == 13) {
            chequear_enviar_mensaje();
        }
    });
    $('#boton-enviar').on('click', function (event) {

        chequear_enviar_mensaje();

	});

    function chequear_enviar_mensaje(){
        var inpTxtMensaje = $('#text-mensaje');
        var texto_enviar = inpTxtMensaje.val();

	    //event.preventDefault();

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
    }
    var chat_txtboard = $('#chat');
    //chat_txtboard.scrollTop(chat_txtboard.prop("scrollHeight"));


});


function crear_mensaje_html(username,mensaje){

    var nueva_entrada = ""
    if($('#username').val() == username){
        nueva_entrada = "<li class='right clearfix'>" +
                    	"<span class='chat-img pull-right'>"
    }else{
        nueva_entrada = '<li class="left clearfix">' +
                    	'<span class="chat-img pull-left">'
    }

    nueva_entrada += '<img src="http://bootdey.com/img/Content/user_3.jpg" alt="User Avatar">' +
                    	'</span>'+
                    	'<div class="chat-body clearfix">'+
                    		'<div class="header">'+
                    			'<strong class="primary-font">' + username + '</strong>'+
                    			//'<small class="pull-right text-muted"><i class="fa fa-clock-o"></i> 12 mins ago</small>'+
                    		'</div>'+
                    		'<p>'+mensaje + '</p>'+
                    	'</div>'+
                    '</li>';


    return nueva_entrada
}
/*
function crear_mensaje_conectado_html(username){
    return '<div><span class="glyphicon glyphicon-user" aria-hidden="true"></span><b> '
        + username +
        ' se ha conectado al chat. </b></div>'
}

function crear_mensaje_desconectado_html(username){
    return '<div><span class="glyphicon glyphicon-user" aria-hidden="true"></span><b> '
        + username +
        ' se ha desconectado del chat. </b></div>'
}

*/