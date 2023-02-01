import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.models import Categoria


def teste(request):
  return HttpResponse('Olá mundo do Django')

@method_decorator(csrf_exempt, name='dispatch')
class CategoriaView(View):
  def get(self, request):
    data = list(Categoria.objects.values())
    formated_data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(formated_data, content_type='application/json')