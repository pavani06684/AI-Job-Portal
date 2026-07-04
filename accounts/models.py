from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES=(
        ("job_seeker","Job Seeker"),
        ("recruiter","Recruiter"),
    )
    role=models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="job_seeker"
    )
    phone_number=models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    profile_picture=models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    def __str__(self):
        return self.username
