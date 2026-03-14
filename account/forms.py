from django import forms
from .models import Employer, Job


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_location', 'company_website']
        widgets = {
                'company_name': forms.TextInput(attrs={'placeholder': 'Enter name'}),
                'company_location': forms.TextInput(attrs={'placeholder': 'Enter location'}),
                'company_website': forms.URLInput(attrs={'placeholder': 'http://google.com'}),
        } 


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'job_title',
            'location',
            'job_type',
            'skills_required',
            'salary',
            'job_description',
        ]
        
        widgets = {
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'style': 'width:100%;'
            })
        }
        