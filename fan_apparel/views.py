from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Product, User, Order, OrderItem, ShippingAddress
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken, OrderSerializer


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from django.contrib.auth.hashers import make_password


# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # loop through fields in serializer and output as data
        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# registration
@api_view(['POST'])
def registerUser(request):
    data = request.data

    # check if the email is already registered
    try: 
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except: 
        message = {'text': 'There is already a user with this email'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# users views
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(["PUT"])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)



# products views
@api_view(["GET"])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProduct(request, pk):
    specificProduct = Product.objects.get(_id=pk)
    serializer = ProductSerializer(specificProduct, many=False)
    return Response(serializer.data)


# order views
@api_view('POST')
@permission_classes([IsAuthenticated])
def addOrderItems(request): 
    user = request.user 
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else: 
        order = Order.objects.create(
            user = user, 
            paymentMethod = data['paymentMethod'], 
            taxPrice = data['taxPrice'], 
            shippingPrice = data['shippingPrice'], 
            totalPrice = data['totalPrice']
        )
        
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country'],
        )

        for i in orderItems: 
            product = Product.objects.get(id=i['product'])

            item = OrderItem.objects.create(
                product = product, 
                order = order, 
                name = product.name, 
                quantity = i['quantity'], 
                price = i['price'], 
                image = product.image.url,
            )

        #update stock count after order
        product.inStock -= item.quantity
        product.save()

        serializer = OrderSerializer(order, many=False)
        return Response('ORDER')