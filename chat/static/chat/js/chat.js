// Note that the path doesn't matter right now; any WebSocket
// connection gets bumped over to WebSocket consumers

socket = new WebSocket("wss://" + window.location.host + "/chat/");
var window_focus;
var nmensajesnoleidos = 0;

$(window).focus(function() {
    window_focus = true;
    nmensajesnoleidos = 0;
    document.title = document.old_title;
}).blur(function() {
    window_focus = false;
});

socket.onmessage = function (message) {

    var data = JSON.parse(message.data);
    var chat = $('#chat');
    var listac = $('#lista-conectados');

    var nconectados = $('#n-conectados');

    if (data.tipo_mensaje == "broadcast") {
        chat.append($(crear_mensaje_html(data.username, data.mensaje)).hide().fadeIn(100));

        if(!window_focus){
            nmensajesnoleidos++;
            document.title = document.old_title + "(" + nmensajesnoleidos + ")";
        }
    }else if(data.tipo_mensaje == "conectado_chat"){
        listac.append($("<li>" + data.username + "</li>").hide().fadeIn(100));
        nconectados.html(parseInt(nconectados.html()) + 1)
    }else if(data.tipo_mensaje == "desconectado_chat"){
        listac.find("li").each(function (index) {
           if($(this).text() == data.username){
               $(this).detach();
               return false;
           }
        });

        if(parseInt(nconectados.html()) > 0)nconectados.html(parseInt(nconectados.html()) - 1)
    }


    if($('#username').val() == data.username){ //Si es un mensaje enviado por el mismo movemos el scroll para abajo
        //Movemos el chat al ultimo elemento enviado - recibido(esperemos sea este)
        $("html, body").animate({ scrollTop: $(document).height()-$(window).height() },200);
    }
};


$(document).ready(function(){

    document.old_title = document.title;

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
