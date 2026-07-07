from django.db import models
from django.conf import settings
# Create your models here.

class Job(models.Model):
    JOB_TYPES=(
        ("full_time",'Full Time'),
        ("part_time","Part Time"),
        ("internship","Internship"),
        ("remote","Remote"),
    )
    title=models.CharField(max_length=200)
    company=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    salary=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    experience=models.PositiveBigIntegerField(help_text="Experience in years")
    job_type=models.CharField(max_length=20,choices=JOB_TYPES,default="full_time")
    description=models.TextField()
    skills=models.TextField(
        help_text="Separate skills with commas"
    )
    recruiter=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="jobs")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title