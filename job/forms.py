from django import forms
from .models import User
import re
from django.contrib.auth import get_user_model,authenticate
from .models import JobApplication

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password']
        widgets = {
                'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
                'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
        }    

    User = get_user_model()
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError("Username must be at least 6 characters")
        alphabets = re.findall(r'[A-Za-z]', username)
        if len(alphabets) < 3:
            raise forms.ValidationError("Username must contain at least 3 letters")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character")

        return password

User = get_user_model()
class LoginForm(forms.Form):
    username = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter username'}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")
        if username:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect password")

        return password
    
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['fullname', 'email', 'phone', 'higher_education', 'percentage', 'resume']

        widgets = {
            'fullname': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'higher_education': forms.TextInput(attrs={'class':'form-control', 'placeholder':'e.g. B.Tech, BSc..'}),
            'percentage': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Percentage'}),
            'resume': forms.FileInput(attrs={'class':'form-control'}),
        }

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        if not fullname:
            raise forms.ValidationError("Enter valid name.")
        fullname = fullname.strip()
        if len(fullname) < 3:
            raise forms.ValidationError("Full name must be at least 3 characters.")
        for word in fullname.split():
            if not word.isalpha():
                raise forms.ValidationError("Name must contain only alphabets.")
        return fullname
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.fullmatch(r'[6-9]\d{9}', phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean_higher_education(self):
        education = self.cleaned_data.get('higher_education')
        if len(education.strip()) < 2:
            raise forms.ValidationError("Enter valid education qualification.")
        return education

    def clean_percentage(self):
        percentage = self.cleaned_data.get('percentage')
        if percentage < 0 or percentage > 100:
            raise forms.ValidationError("Percentage must be between 0 and 100.")
        return percentage

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError("Resume must be in PDF format.")        
        return resume