from django.db import models
from django.contrib.auth.models import AbstractUser
from account.models import Job
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES=(
        ('employee','Employee'),
        ('employer','Employer'),
        
    )
    user_type=models.CharField(max_length=10,choices=USER_TYPE_CHOICES)

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    higher_education = models.CharField(max_length=100)   
    percentage = models.FloatField()                       
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname