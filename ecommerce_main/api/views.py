from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login,logout
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password 
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
import json
# Create your views here.

@api_view(["GET"])
def filter_products(request,field,query):
    products = []
    if field == "category":
        category_ins = Category.objects.get(name=query)
        products = Product.objects.filter(category=category_ins)
    elif field == "gender":
        gender_ins = Gender.objects.get(name=query)
        products = Product.objects.filter(gender=gender_ins)
    elif field == 'name':
        products = Product.objects.filter(name__icontains=query)

    data = ProductSerializer(products,many=True)
    return Response(data.data)

@api_view(['GET'])
def get_product(request,id):
    product = Product.objects.get(id=id)
    data = ProductSerializer(product)

    return Response(data.data)

@api_view(['GET'])
def add_product_to_cart(request,user_id,product_id):
    user = Profile.objects.get(user_id=user_id)
    product = Product.objects.get(id=product_id)
    user.cart.add(product)

    return Response("Successfully addded product to cart")


@api_view(['GET'])
def remove_product_from_cart(request,user_id,product_id):
    user = Profile.objects.get(user_id=user_id)
    product = Product.objects.get(id=product_id)
    user.cart.remove(product)

    return Response("Successfully removed product from cart")


@api_view(["GET"])
def get_my_cart(request,user_id):
    user = Profile.objects.get(user_id=user_id)
    cart_items = user.cart.all()
    data = ProductSerializer(cart_items,many=True)

    return Response(data.data)


@api_view(['GET'])
def place_order(request,buyer_id,product_id):
    product = Product.objects.get(id=product_id)
    profile = Profile.objects.get(user_id=buyer_id)
    order = Order.objects.create(buyer=profile, product=product)
    
    profile.my_orders.add(order)

    return Response("Successfully placed order")


@api_view(['GET'])
def cancel_order(request,order_id):
    order = Order.objects.get(id=order_id)
    order.is_cancelled = True
    order.save()    

    return Response("Successfully cancelled order")


@api_view(['GET'])
def get_my_orders(request,user_id):
    profile = Profile.objects.get(user_id=user_id)
    orders = profile.my_orders.all()
    data = OrderSerializer(orders,many=True)

    return Response(data.data)


@api_view(['GET'])
def get_my_profile(request,user_id):
    profile = Profile.objects.get(user_id=user_id)
    data = ProfileSerializer(profile)

    return Response(data.data)

@api_view(['GET'])
def delete_user(request,user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(True)
    except User.DoesNotExist:
        return Response(False)

    


@api_view(['POST'])
def register(request):
    username = request.POST.get('username').replace(" ","_")
    email = request.POST.get('email')
    password = request.POST.get('password')
    hased_password = make_password(password)
    if User.objects.filter(username=username, email=email).count() > 0:
        return Response("There is already a user registered with this username and email.")
    else:
        user = User.objects.create(username=username, email=email,password=hased_password)
        Profile.objects.create(user_id=user.id)
        token = Token.objects.create(user=user).key
        login(request._request,user=user)
        return Response({"token": token})


@api_view(['POST'])
def login_user(request):
    password = request.POST.get('password')
    email_username = request.POST.get('email_username')

    if '@' in email_username:
        username = User.objects.get(email=email_username).username
        user = authenticate(request._request,username=username,password=password)
        
        if user is not None:
            login(request._request,user)
            token,created = Token.objects.get_or_create(user=user)
            return Response({"token":token.key})
        else:
            return Response("The email or password you entered is incorrect or does'nt exist")
    
    else:
        user = authenticate(username=email_username,password=password)
        if user is not None:
            
            token,created = Token.objects.get_or_create(user=user)
            return Response({"token":token.key})
        else:
            return Response("The email or password you entered is incorrect")



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        logout(request._request)
        return Response(True)
    except:
        return Response(False)

    

@api_view(['GET'])
def check_username_existence(request):
    username = request.GET.get('username')
    

    try:
        User.objects.get(username=username)
        return Response(True)
    except User.DoesNotExist:
        return Response(False)
    
@api_view(['GET'])
def check_email_existence(request):
    email = request.GET.get('email')
    user = User.objects.get(email=email)

    if user:
        return Response(True)
    else:
        return Response(False)
    
@api_view(['GET'])
def check_password(request):
    password = request.GET.get('password')
    user_id = request.GET.get('user_id')
    
    try:
        user = User.objects.get(id=user_id)
        is_valid = user.check_password(password)
        return Response(is_valid)
    except User.DoesNotExist:
        return Response(False)


@api_view(['POST'])
def set_password(request):
    uidb64 = request.POST.get("uidb64")
    user = None
    password = request.POST.get("password")

    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        UserModel = get_user_model()
        user = UserModel._default_manager.get(pk=uid)
    except:
        user = None
    for x in range(10):
        print(uidb64)
    if user is not None:
        user.set_password(password)
        user.save()
        return Response(True)
    else:
        return Response(False)
    
@api_view(['POST'])
def change_address(request):
    current_address = Address.objects.get(id=request.POST.get('current_address_id'))
    name = request.POST.get('name')
    phone_number = request.POST.get('phone_number')
    house_name = request.POST.get('house_name')
    street_name = request.POST.get('street_name')
    state_name = request.POST.get('state_name')
    pincode = request.POST.get('pincode')
    landmark = request.POST.get('landmark')
    town_city = request.POST.get('town_city')
  

    current_address.name = name
    current_address.phone_number = phone_number
    current_address.house_name = house_name
    current_address.street_name = street_name
    current_address.state_name = state_name
    current_address.pincode = pincode
    current_address.landmark = landmark
    current_address.town_city =town_city

    current_address.save()

    return Response(True)