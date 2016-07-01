from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .forms import DatosRegistroUsuarioChat


def crear_cuenta(request):
	
	if request.method == "POST":
		form = DatosRegistroUsuarioChat(request.POST)

		if form.is_valid():
			
			contra = form.cleaned_data['password']
			contra_confirmada = form.cleaned_data['password_confirmar']

			if contra == contra_confirmada:
				return HttpResponse('OK!')
			else:
				form.add_error("password_confirmar", "Las contraseñas no coinciden.")
	else:
		form = DatosRegistroUsuarioChat()
	return render(request, 'registration/signup.html', {'form':form})

