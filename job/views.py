from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,JobApplicationForm
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm
from account.models import Job
from .models import JobApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def home(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request,'home.html',context={'jobs':jobs})

def register(request):
    msg=''
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user= form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            msg='Signup Comleted Successfully'
            form = RegisterForm()
        else:
            print(form.errors) 

    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form,'msg':msg})


def user_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request,user)
                # reading user type
                if user.user_type == "employer":
                    return redirect('employer_dashboard')

                if user.user_type == "employee":
                    return redirect('home')              
    return render(request, 'login.html', {'form': form})

@login_required
def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'job_detail.html', {'job': job})

def logout_view(request):
    logout(request)
    return redirect('home')

def apply_job(request, id):
    job = get_object_or_404(Job, id=id)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You already applied for this job")
        return redirect('job_detail', id=id)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Job applied successfully")
            return redirect('job_detail',id=id)

    else:
        form = JobApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})

@login_required
def job_search(request):
    keyword = request.GET.get('keyword')
    location = request.GET.get('location')
    jobs = Job.objects.all()
    if keyword:
        jobs = jobs.filter(
            Q(job_title__icontains=keyword) |
            Q(employer__company_name__icontains=keyword)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)
    return render(request, 'home.html', context={'jobs':jobs})