from django.shortcuts import render,redirect
from api.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.contrib.auth import login,authenticate,logout
import requests



def mail(message,recipient_list):
    email = EmailMessage(
    'From PITBULL',
    message,
    settings.EMAIL_HOST_USER,
    recipient_list,
    )

    email.send(fail_silently=False)

# Create your views here.
def home(request):
    if request.method == 'POST':
        query = request.POST.get('search-input')
        return redirect("search_result_screen" ,query)
    
    categories = Category.objects.all()

    return render(request, 'ecommerce/index.html',context={
        "categories": categories,
    })


@login_required(login_url="login_screen")
def profile_screen(request):
    if request.method == 'POST':
        logout(request)
        return redirect("home")
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request,'ecommerce/profile.html',context={
        "profile": profile
    })

@login_required(login_url='login_screen')
def my_cart_screen(request):
    profile = Profile.objects.get(user_id=request.user.id)
   
    return render(request,'ecommerce/myCart.html',context={
        "cart": profile.cart.all()
    })

def view_product_screen(request,product_id):
    product = Product.objects.get(id=product_id)
    return render(request,'ecommerce/viewProduct.html',context={
        "product": product
    })


def search_result_screen(request,query):
    results = Product.objects.filter(name__icontains=query)  #requests.get(f"http://127.0.0.1:8000/api/filter_products/name/{query}/").json()
    return render(request,'ecommerce/SearchResultScreen.html',context={
        "result": results,
        "query": query
    })



def login_screen(request):
    
    if request.method == 'POST':
        email_username = request.POST.get('email_username')
        password = request.POST.get('password')
    
        if '@' in email_username:
            username = User.objects.get(username=email_username).username
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                messages.error(request,"The user credentials you provided is incorrect")
        else:
            user = authenticate(request,username=email_username,password=password)
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                messages.error(request,"The user credentials you provided is incorrect")

    return render(request,'ecommerce/auth/LoginScreen.html')

def register_screen_1(request):    
    return render(request,'ecommerce/auth/register/NameEmailScreen.html')

def register_screen_2(request,username,email):
    return render(request,'ecommerce/auth/register/PasswordScreen.html',context={
        "email": email,
        "username": username
    })

@login_required(login_url="login_screen")
def previous_orders_screen(request):
    profile = Profile.objects.get(user_id=request.user.id)
    orders = Order.objects.filter(buyer=profile)
    print(Profile.objects.get(user_id=request.user.id).my_orders)
    return render(request,"ecommerce/PreviousOrdersScreen.html",context={
        "orders": orders
    })

@login_required(login_url="login_screen")
def place_order_screen(request,product_id):
    product = Product.objects.get(id=product_id)
    return render(request,"ecommerce/place_order/ConformOrder.html",context={
        "product": product
    })

@login_required(login_url="login_screen")
def place_order_screen_address(request,product_id):

    if request.method == "POST":
        name = request.POST.get("name")
        phone_number = request.POST.get("number")
        house_name = request.POST.get("house_no")
        street_name = request.POST.get("street")
        state_name = request.POST.get("state")
        pincode = request.POST.get("pincode")
        landmark = request.POST.get("landmark")
        town_city = request.POST.get("town_city")
        save_address = request.POST.get("save_address")

        
        if len(pincode) != 6 or not pincode.isnumeric():
            messages.error(request, "Please enter a valid PINCODE")
        elif len(phone_number) != 10 or not phone_number.isnumeric():
            messages.error(request, "Please enter a valid phone number")
        else:
            buyer = Profile.objects.get(user_id=request.user.id)
            
            if save_address is not None:
                url = request.scheme + '://' + request.get_host() + '/api/change-address'
                data = {
                    "name" : name,
                    "phone_number" : phone_number,
                    "house_name" : house_name,
                    "street_name" : street_name,
                    "state_name" : state_name,
                    "pincode" : pincode,
                    "landmark" : landmark,
                    "town_city" : town_city,
                    "current_address_id" : buyer.address.id
                }
                
                requests.post(url,data=data)
                

            product = Product.objects.get(id=product_id)
            order = Order.objects.create(buyer=buyer,product=product,delivery_address=buyer.address)

            return redirect("order_placed_success",order.id)


    default_address = Profile.objects.get(user_id=request.user.id).address
    return render(request,"ecommerce/place_order/DeliveryAddress.html",context={
            "address": default_address
    })

@login_required(login_url="login_screen")
def order_placed_success(request,order_id):
    order = Order.objects.get(id=order_id)
    return render(request,"ecommerce/place_order/order_placed.html",context={
    "order": order
    })


def category_products(request,category_id):
    category = Category.objects.get(id=category_id)
    return render(request,"ecommerce/CategoryProducts.html/",context={
        "category": category
    })



def password_reset(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            entered_email = request.POST.get('email')
            associated_users = User.objects.filter(email=entered_email)
            if associated_users.exists():
                for user in associated_users:
                    contexts = {
                        "email":user.email,
                        'domain':request.META['HTTP_HOST'],
                        'site_name': 'PITBULL',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    content = render_to_string('change-password/mail-content.txt',contexts)
                    mail(content,[user.email])
                    
                    return redirect('password_reset_done')
            else:
                messages.error(request,"The email you entered does'nt exists")
    password_reset_form = PasswordResetForm()
    return render(request,'change-password/change-password.html',{"form":password_reset_form})


def set_password(request,uidb64,token):
    return render(request,'change-password/new-password.html',context={
        "uidb64":uidb64,
    })