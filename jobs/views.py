from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job
from django.db.models import Q
from django.http import HttpResponse
from applications.models import Application
# Create your views here.

@login_required
def create_job(request):
    if request.method=="POST":
        form=JobForm(request.POST)
        if form.is_valid():
            job=form.save(commit=False)
            job.recruiter=request.user
            job.save()

            return redirect("dashboard")
    else:
        form=JobForm()
    return render(request,"jobs/create_job.html",{"form":form})

def job_list(request):
    search=request.GET.get("search")
    location=request.GET.get("location")
    job_type=request.GET.get("job_type")

    
    jobs=Job.objects.all().order_by("-created_at")
    #search
    if search:
        jobs=jobs.filter(Q(title__icontains=search) | Q(company__icontains=search) | Q(skills__icontains=search))
    # filter by location
    if location:
        jobs=jobs.filter(location__icontains=location)
    if job_type:
        jobs=jobs.filter(job_type=job_type)
    return render(request,"jobs/job_list.html",{
        "jobs":jobs,
        "search":search,
        "location":location,
        "job_type":job_type,

    })
    

def job_detail(request,job_id):
    job=get_object_or_404(Job,id=job_id)
    return render(request,"jobs/job_detail.html",{"job":job})

@login_required
def edit_job(request,job_id):
    if request.user.role != "recruiter":
        return HttpResponse("Access Denied!")
    job=get_object_or_404(Job,id=job_id)
    if request.method=="POST":
        form=JobForm(request.POST,instance=job)
        if form.is_valid():
            updated_job=form.save(commit=False)
            updated_job.recruiter=job.recruiter
            updated_job.save()
            return redirect("job_detail",job_id=job.id)
    else:
        form=JobForm(instance=job)
    return render(request,"jobs/edit_job.html",{"form":form,"job":job})

@login_required
def delete_job(request,job_id):
    if request.user.role != "recruiter":
        return HttpResponse("Access Denied!")
    job=get_object_or_404(Job,id=job_id)
    if request.method=="POST":
        job.delete()
        return redirect("job_list")
    return render(request,"jobs/delete_job.html",{"job":job})


@login_required
def recruiter_dashboard(request):

    if request.user.role != "recruiter":
        return HttpResponse("Access Denied!")

    jobs = Job.objects.filter(
        recruiter=request.user
    ).order_by("-created_at")

    applications = Application.objects.filter(
        job__recruiter=request.user
    )

    context = {
        "jobs": jobs,
        "total_jobs": jobs.count(),
        "total_applications": applications.count(),
        "pending": applications.filter(status="Pending").count(),
        "shortlisted": applications.filter(status="Shortlisted").count(),
        "rejected": applications.filter(status="Rejected").count(),
    }

    return render(
        request,
        "jobs/recruiter_dashboard.html",
        context
    )

