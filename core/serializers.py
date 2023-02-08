from django.contrib.auth.models import User
from rest_framework.serializers import (CharField, ModelSerializer,
                                        SerializerMethodField)

from .models import Autor, Categoria, Compra, Editora, Livro, ItensCompra


class CategoriaSerializer(ModelSerializer):
  class Meta:
    model = Categoria
    fields = '__all__'

class EditoraSerializer(ModelSerializer):
  class Meta:
    model = Editora
    fields = '__all__'

class EditoraNestedSerializer(ModelSerializer):
  class Meta:
    model = Editora
    fields = ('nome',)

class AutorSerializer(ModelSerializer):
  class Meta:
    model = Autor
    fields = '__all__'

class LivroSerializer(ModelSerializer):
  class Meta:
    model = Livro
    fields = '__all__'

class LivroDetailSerializer(ModelSerializer):
  categoria = CharField(source='categoria.descricao')
  editora = EditoraNestedSerializer()
  autores = SerializerMethodField()
  
  class Meta:
    model = Livro
    fields = '__all__'
    depth = 1

  def get_autores(self, obj):
   nomes_autores = []
   autores = obj.autores.get_queryset() 
   for autor in autores:
    nomes_autores.append(autor.nome)
   
   return nomes_autores

# Compra

class ItensCompraSerializer(ModelSerializer):
  total = SerializerMethodField()
  class Meta:
    model = ItensCompra
    fields = ('livro', 'quantidade', 'total')
    depth = 1

  def get_total(self, obj):
    return obj.quantidade * obj.livro.preco
    

class CompraSerializer(ModelSerializer):
  usuario = CharField(source='usuario.email')
  status = SerializerMethodField()
  itens = ItensCompraSerializer(many=True)
  class Meta:
    model = Compra
    fields = '__all__'
    
  
  def get_status(self, obj):
    return obj.get_status_display()