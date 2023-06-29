from django.shortcuts import render,redirect
from .forms import UserRegisterForm,CategoryForm,ProductForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Category,Product,Cart,Order
from django.views.generic import ListView
from django.contrib import messages
import json
from django.http import  JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.

def base(request):

    return render(request ,'base.html')


def register(request):

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit = False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username =user.username,password =password)
        auth_login(request, new_user)
        return redirect('login')

    context = {
        'form' : form
    }

    return render(request,'eapp_temp/register.html',context)



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_staff:
                    return redirect('adminhome')
                else:
                    return redirect('userhome')

    else:
        form = AuthenticationForm()
    
    context = {
        'form': form
    }
    return render(request, 'eapp_temp/login.html', context)



def index(request):
    
    category = Category.objects.filter(status = 0)


    context = {
        'category':category
    }

  

    return render(request ,'eapp_temp/index.html',context)


@login_required(login_url = "/login")

def adminhome(request):


    return render(request, 'eapp_temp/adminhome.html')

def admin_add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('admin_add_category')
    else:
        form = CategoryForm()

    context = {"form": form}
    return render(request, 'eapp_temp/add_category.html',context)


def admin_add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('admin_add_product')
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, 'eapp_temp/add_product.html',context)



@login_required(login_url ="/login")
def userhome(request):

    category = Category.objects.filter(status = 0)

    context = {
        'category':category
    }

    return render(request ,'eapp_temp/userhome.html',context)

def productview(request,name):
  if(Category.objects.filter(name=name,status=0)):
      products=Product.objects.filter(Category__name=name)
      return render(request,"eapp_temp/products.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('userhome')



def productdetails(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"eapp_temp/productdetails.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('userhome')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('userhome')




def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']

            product_status = get_object_or_404(Product, id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        product_status.quantity -= product_qty
                        product_status.save()
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)



def cart_page(request):
    cart=Cart.objects.filter(user=request.user)

    context = {
        "cart":cart
    }

    print(context)
    return render(request,"eapp_temp/show_cart.html",context)


def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart_page")


def userprofile(request):

    user = request.user
    context = {
        "user": user
    }
    return render(request,"eapp_temp/user_profile.html",context)




def order_view(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        "orders": orders
    }
    return render(request, "eapp_temp/orderview.html", context)

def place_order(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        print(cart_items)
        if cart_items.exists():
            for cart_item in cart_items:
                Order.objects.create(user=request.user, product=cart_item.product, quantity=cart_item.product_qty)
            cart_items.delete()
            return JsonResponse({'status': 'Order placed successfully'}, status=200)
        else:
            return JsonResponse({'status': 'No items in the cart'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid request method'}, status=400)
