from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .forms import ApplicationForm
from .models import Application
from jobs.models import Job


# Apply for a Job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only Job Seekers can apply
    if request.user.role != "job_seeker":
        return HttpResponse("Only Job Seekers can apply for jobs.")

    # Prevent duplicate applications
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_detail", job_id=job.id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            messages.success(request, "Application submitted successfully!")
            return redirect("job_detail", job_id=job.id)

    else:
        form = ApplicationForm()

    return render(request, "applications/apply_job.html", {
        "form": form,
        "job": job,
    })


# Recruiter - View Applications
@login_required
def view_applications(request, job_id):

    if request.user.role != "recruiter":
        return HttpResponse("Access Denied!")

    job = get_object_or_404(Job, id=job_id)

    applications = Application.objects.filter(job=job)

    return render(request, "applications/view_applications.html", {
        "job": job,
        "applications": applications,
    })


# Recruiter - Update Application Status
@login_required
def update_status(request, application_id):

    if request.user.role != "recruiter":
        return HttpResponse("Access Denied!")

    application = get_object_or_404(Application, id=application_id)

    if request.method == "POST":
        application.status = request.POST.get("status")
        application.save()

        messages.success(request, "Application status updated successfully!")

    return redirect("view_applications", job_id=application.job.id)


# Job Seeker - View My Applications
@login_required
def my_applications(request):

    if request.user.role != "job_seeker":
        return HttpResponse("Access Denied!")

    applications = Application.objects.filter(
        applicant=request.user
    ).order_by("-applied_at")

    return render(request, "applications/my_applications.html", {
        "applications": applications,
    })
    