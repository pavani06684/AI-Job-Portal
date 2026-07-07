from django.urls import path
from . import views

urlpatterns=[
    path("apply/<int:job_id>/",views.apply_job,name="apply_job"),
    path("job/<int:job_id>/applications/",views.view_applications,name="view_applications"),
    path("update-status/<int:application_id>/",views.update_status,name="update_status"),
    path("my-applications/",views.my_applications,name="my_applications"),
]