from django.urls import path
from . import views

urlpatterns=[
    path("resume-analyzer/",views.analyze_resume,name="resume_analyzer"),
]