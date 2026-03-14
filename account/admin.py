from django.contrib import admin
from .models import Employer, Job

class EmployerAdmin(admin.ModelAdmin):
    list_display=('id','company_name','company_location','company_website','user_id')
    search_fields=['company_name','company_location']

class JobAdmin(admin.ModelAdmin):
    list_display=('id','job_title','location','job_type','skills_required','salary','created_at','job_description','employer_id')
    search_fields=['job_title','location']

admin.site.register(Employer,EmployerAdmin)
admin.site.register(Job,JobAdmin)

