from django.contrib import admin
from .models import User,JobApplication
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('id','username','email','is_superuser','is_staff','user_type','password')
    search_fields=['username']

class JobApplicationAdmin(admin.ModelAdmin):
    list_display=('id','fullname','email','phone','higher_education','percentage','resume','applied_at','applicant','job')
    search_fields=['fullname']

admin.site.register(User,UserAdmin)
admin.site.register(JobApplication,JobApplicationAdmin)

