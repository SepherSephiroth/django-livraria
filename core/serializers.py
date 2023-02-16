from django.contrib.auth.models import User
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from rest_framework import serializers

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
    fields = ('id', 'usuario', 'status', 'itens', 'total')
    
  
  def get_status(self, obj):
    return obj.get_status_display()
  

class CriarEditarItensCompraSerializer(ModelSerializer):
  class Meta:
    model = ItensCompra
    fields = ('livro','quantidade')


class CriarEditarCompraSerializer(ModelSerializer):
  itens = CriarEditarItensCompraSerializer(many=True)
  usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
  class Meta:
    model = Compra
    fields = ('id', 'usuario', 'itens')

  def create(self, validated_data):
    itens = validated_data.pop('itens')
    compra = Compra.objects.create(**validated_data)
    for item in itens:
      ItensCompra.objects.create(compra=compra, **item)
    compra.save()

    return compra
  
  def update(self, instance, validated_data):
    itens = validated_data.pop('itens')
    if itens:
      instance.itens.all().delete()
      for item in itens:
        ItensCompra.objects.create(compra=instance, **item)
      instance.save()
    
    return instance
