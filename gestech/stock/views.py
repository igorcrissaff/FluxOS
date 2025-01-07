from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

def index(request):
    return 'index'

def get(request, codigo):
    produto = Product.objects.get(codigo=codigo)
    return JsonResponse(produto.to_json())

def get_all(request):
    produtos = Product.objects.all()
    return JsonResponse([produto.to_json() for produto in produtos], safe=False)
