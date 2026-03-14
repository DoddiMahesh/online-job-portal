from django.db import models
from django.conf import settings
# Create your models here.

class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_location = models.CharField(max_length=200)
    company_website = models.URLField(blank=True)

    def __str__(self):
        return self.company_name
    
class Job(models.Model):
    JOB_TYPE_CHOICES=(
        ('Full-Time','Full-Time'),
        ('Part-Time','Part-Time'),
        ('Internship','Internship'),
    )
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE) 
    job_title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=10,choices=JOB_TYPE_CHOICES)
    skills_required = models.CharField(max_length=300)
    salary = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    job_description =models.TextField()

    def __str__(self):
        return self.job_title
