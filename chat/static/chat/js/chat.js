// Submit post on submit

$(document).ready(function(){

	$('#form-mensaje').on('submit', function(event){
	    event.preventDefault();
        var texto_enviar = $('#inpTxtMensaje').val();
        if(texto_enviar){
            if(texto_enviar.trim().length > 0){
                enviar_mensaje_chat();
            }else{
                $('#inpTxtMensaje').val(''); // remove the value from the input
            }
        }
        
	});

    $('#chat-txtboard').scrollTop($('#chat-txtboard').prop("scrollHeight"));

	// AJAX for posting
	function enviar_mensaje_chat() {
	    $.ajax({
	        url : "enviarMensaje/", // the endpoint
	        type : "POST", // http method
	        data : { mensaje : $('#inpTxtMensaje').val() }, // data sent with the post request

	        // handle a successful response
	        success : function(json) {

	        	//Limpiamos el chat
	            $('#inpTxtMensaje').val(''); // remove the value from the input

	            //var chat = $('#chat-txtboard');
	            //Agregamos el mensaje al chat
	            //chat.append(crear_mensaje_html(json.username,json.mensaje));

	            //Movemos el chat al ultimo elemento enviado - recibido(esperemos sea este)
	            //chat.scrollTop(chat.prop("scrollHeight"));
	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	        }
    	});
	};
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

(function updater() {
  $.ajax({
    url: 'recibirActualizaciones', 
    type:"GET",
    success: function(json) {
        var chat = $('#chat-txtboard');

        if(json.mensajes.length > 0){
            for (var i = 0; i < json.mensajes.length; i++) {

                if(json.mensajes[i].tipo == 'mensaje_usuario'){
                    chat.append(crear_mensaje_html(json.mensajes[i].username,json.mensajes[i].mensaje));
                }else if(json.mensajes[i].tipo == 'mensaje_inicio_sesion'){                    
                    chat.append(crear_mensaje_inicio_sesion_html(json.mensajes[i].username));
                }
            }

            //Movemos el chat al ultimo elemento enviado - recibido(esperemos sea este)
            chat.scrollTop(chat.prop("scrollHeight"));
        }
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(updater, 500);
    }
  });
})();

function crear_mensaje_html(username,mensaje){
    return '<div><span class="glyphicon glyphicon-user" aria-hidden="true"></span><b> ' + username + ': </b>' + 
                    mensaje + '</div>'
}

function crear_mensaje_inicio_sesion_html(username){
    return '<div><span class="glyphicon glyphicon-user" aria-hidden="true"></span><b> ' + username + ' ha iniciado sesión. </b></div>'
}

