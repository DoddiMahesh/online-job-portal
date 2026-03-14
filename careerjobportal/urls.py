"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from job.views import home,register,user_login,job_detail,logout_view,apply_job,job_search
from account.views import employer_dashboard,employer_profile,post_job,employer_job_detail,edit_job,delete_job,job_applications,employer_job_search
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('register/',register),
    path('login/',user_login),
    path('logout/',logout_view),
    path('employer_dashboard/',employer_dashboard,name='employer_dashboard'),
    path('employer_profile/',employer_profile,name='employer_profile'),
    path('post_job/',post_job),
    path('job_detail/<int:id>/',job_detail, name='job_detail'),
    path('employer_job_details/<int:id>/',employer_job_detail,name="employer_job_details"),
    path('edit_job/<int:id>/',edit_job,name='edit_job'),
    path('delete_job/<int:id>/',delete_job,name='delete_job'),
    path('apply_job/<int:id>/',apply_job, name='apply_job'),
    path('job_applications/<int:id>/',job_applications, name='job_applications'),
    path('job_search/',job_search,name='job_search'),
    path('employer_job_search/',employer_job_search,name='employer_job_search'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

