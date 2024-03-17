from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import *
from .cart import Cart
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse
# Create your views here.


def index(request):
    products = Ecommerce_Product.objects.all()
    context = {
        'products' : products
    }
    return render(request,'app1/index.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in'))
            return redirect('index')
        else:
            messages.success(request, ("Please try again!"))
            return redirect('login')
    else:
        return render(request,'app1/login.html', )


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('index')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, 'Please try again!')
    else:

        return render(request,'app1/register.html', {'form': form})

@login_required
def cart_summary(request):

    cart = Cart(request)
    cart_products = cart.get_prods
    totals = cart.cart_total()
    return render(request, "app1/cart/cart_summary.html",
                  {'cart_products': cart_products, "totals": totals})
@login_required
def view_item(request,pk):
    product = Ecommerce_Product.objects.get(id=pk)

    return render(request, 'app1/view_item.html', {'product': product})


@login_required
def add_cart_item(request):
    # Gert Cart

    cart = Cart(request)
    # Test for post
    print('cart', cart)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        print('Product id',product_id)
        # lookup product in the db
        product_quantity = int(request.POST.get('product_qty'))
        product = get_object_or_404(Ecommerce_Product, id=product_id)

        cart.add(product=product, quantity=product_quantity)
        #response = JsonResponse({'Product Name': product.name})
        cart_quantity = cart.__len__()
        print(cart_quantity)
        response = JsonResponse({'Qty': cart_quantity})
        return response
    return render(request, "app1/cart/add_cart_item.html")

def delete_cart_item(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        # Call delete Fucntion

        cart.delete(product=product_id)
        response = JsonResponse({'Product': product_id})
        return response


def update(request):
    return render(request, "app1/cart/update_cart.html")


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User Has Been Updated!")
            return redirect('index')
        return render(request, 'app1/update_user.html', {'user_form': user_form})
    else:
        messages.success(request, "User Must be Logged in!")
        return redirect('index')
def payment_success(request):
    return render(request, "app1/payment/payment.html")



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangeUserPasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "User Password Changed")
                login(request, current_user)
                return redirect('index')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

            #return render(request, 'app1/update_password.html')
        else:
            form = ChangeUserPasswordForm(current_user)
            context = {
                'form': form
            }
            return render(request, 'app1/update_password.html', context)
    else:
        messages.success(request, "User Must be Logged in!")
        return redirect('index')

def category_summary(request):
    pass

def categories(request,foo):
    foo = foo.replace('-',' ')

    try:
        category = Ecommerce_Category.objects.get(name=foo)
        products = Ecommerce_Product.objects.filter(category=category)
        context = {
            'products': products,
            'category': category
        }
        return render(request, 'app1/category.html',context )


    except:
        messages.success(request,'That category does not exist.')
        return redirect('index')

@login_required
def profile(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            #login(request, current_user)
            messages.success(request, "Your Information has Been updated")
            return redirect('index')
        return render(request, 'app1/profile.html', {'form': form})
    else:
        messages.success(request, "User Must be Logged in!")
        return redirect('index')


def payment(request):
    return render(request, 'app1/payment/payment.html')


def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        search = Ecommerce_Product.objects.filter(name__icontains=search)
        if not search:
            messages.success(request, "That product does not exist!")
            return render(request, 'app1/search.html',)
        else:

            context = {
                'search': search
            }
            return render(request, 'app1/search.html', context)

    else:
        return render(request, 'app1/search.html')