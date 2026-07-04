from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method== "POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form=RegisterForm()
    return render(request,"accounts/register.html",{"form":form})

def user_login(request):
    if request.method== "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(
            request,
            username=username,
            password=password


        )
        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:
            messages.error(request,"Invalid username or password")
    return render(request,"accounts/login.html")

@login_required
def dashboard(request):
    return render(request,"accounts/dashboard.html")
