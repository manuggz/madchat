from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


def index(request):
    return render(request, 'chat/index.html', None)


def enviarMensaje(request):
	if request.method == 'POST':
		msg = request.POST.get('mensaje')
		return JsonResponse({'username':'manuggz','mensaje':msg})
	else:
		return JsonResponse({'fail':'lul'})