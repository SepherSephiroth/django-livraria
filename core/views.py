from django.http import HttpResponse


def teste(request):
  return HttpResponse('Olá mundo do Django')