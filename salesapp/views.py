from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.

@login_required(login_url='/accounts/login/')
def home(request):
    products = Products.objects.all()
    context = {
    "products":products,
    }
    return render(request, 'index.html', locals())

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form':form,
    }
    return render(request, 'registration/register.html', context)


@login_required(login_url='/accounts/login/')
def profile(request):
    products = Products.objects.all()
    posts = Profile.objects.all()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been successfully updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'user_form':user_form,
    'profile_form':profile_form,
    'posts':posts,
    'products':products,
    }
    return render(request, 'profile/profile.html', context)


@login_required(login_url='/accounts/login/')
def updateprofile(request):
    products = Products.objects.all()
    posts = Profile.objects.all()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been successfully updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'user_form':user_form,
    'profile_form':profile_form,
    'posts':posts,
    'products':products,
    }

    return render(request, 'profile/update_profile.html', context)


@login_required(login_url='/accounts/login/')
def postproduct(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = current_user
            product.save()
        return redirect('/')
    else:
        form = ProductForm()
    context = {
        'form':form,
    }
    return render(request, 'PostProduct.html', context)

@login_required(login_url='/accounts/login/')
def get_product(request, id):
    product = Products.objects.get(pk=id)

    return render(request, 'product.html', {'product':product})

@login_required(login_url='/accounts/login/')
def search_products(request):
    if  request.method == "GET": 
        search_term = request.GET.get("search")
        searched_products = Products.search_products(search_term)
        message = f"{search_term}"
        
        return render(request, 'search.html', {"message":message, "products": searched_products})
    else:
        message = "You haven't searched for any user"

        return render(request, 'search.html', {"message":message})