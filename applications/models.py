from django.db import models
from django.conf import settings
from jobs.models import Job 
# Create your models here.

class Application(models.Model):
    STATUS_CHOICES=(
        ("Pending","Pending"),
        ("Shortlisted","Shortlisted"),
        ("Rejected","Rejected"),
        ("Hired","Hired"),
    )
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    applicant=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    resume=models.FileField(upload_to="resume/")
    cover_letter=models.TextField(blank=True)
    status=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    applied_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
