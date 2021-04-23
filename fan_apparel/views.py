from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Product
from .products import products
from .serializers import ProductSerializer


# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        # routes that will be used later
        '/api/products/',
        '/api/products/create/',
        '/api/products/upload/',
        '/api/products/<update>/<id>/',
        '/api/products/delete/<id>/',
        '/api/products/<id>/',
    ]
    return Response(routes)


@api_view(["GET"])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProduct(request, pk):
    specificProduct = None
    for product in products:
        if product['_id'] == pk:
            specificProduct = product
            break

    return Response(product)
