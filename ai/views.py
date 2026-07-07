from django.shortcuts import render
from .utils import (extract_text_from_pdf, extract_skills,calculate_resume_score,calculate_job_match,)
from jobs.models import Job
# Create your views here.

def analyze_resume(request):
    jobs=Job.objects.all()
    result=None
    if request.method=="POST":
        pdf=request.FILES.get("resume")
        job_id=request.POST.get("job")
        if pdf and job_id:
            job=Job.objects.get(id=job_id)
            with open("temp_resume.pdf","wb+") as destination:
                for chunk in pdf.chunks():
                    destination.write(chunk)
            text=extract_text_from_pdf("temp_resume.pdf")
            skills=extract_skills(text)
            score=calculate_resume_score(skills)
            match_percentage,matched_skills,missing_skills=calculate_job_match(skills,job.skills)
            result={
                "skills":skills,
                "score":score,
                "match_percentage":match_percentage,
                "matched_skills":matched_skills,
                "missing_skills":missing_skills,
                "job":job,

            }
    return render(request,"ai/analyze_resume.html",{
        "jobs":jobs,
        "result":result,
    })