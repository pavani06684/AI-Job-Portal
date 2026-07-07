from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .profile_forms import ProfileForm
from jobs.models import Job
from .models import User

# Create your views here.
def home(request):
    total_jobs=Job.objects.count()
    total_recruiters=User.objects.filter(role="recruiter").count()
    total_job_seekers=User.objects.filter(role="job_seeker").count()
    context={
        "total_jobs":total_jobs,
        "total_recruiters":total_recruiters,
        "total_job_seekers":total_job_seekers,
    }
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


@login_required
def profile(request):
    if request.method== "POST":
        form=ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user

        )

        if form.is_valid():
            form.save()
            messages.success(request,"profile updated successfully!")
            return redirect("profile")
    else:
        form=ProfileForm(instance=request.user)
    return render(request,"accounts/profile.html",
                  {"form":form})

def user_logout(request):
    logout(request)
    return redirect("home")

