from rest_framework.serializers import (CharField, ModelSerializer,
                                        SerializerMethodField)

from .models import Autor, Categoria, Editora, Livro


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
