from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
	return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:  # Check if authentication was successful
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There was an error, please try again...")
            return redirect('login')
    else:
      return render(request, 'login.html', {})




def logout_user(request):
      logout(request)
      messages.success(request, ("You have been logged out...Thanks for stopping by"))
      return redirect('home')

def register_user(request):
     return render(request, 'register.html', {})
