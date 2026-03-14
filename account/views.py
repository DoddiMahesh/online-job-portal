from django.shortcuts import render,redirect,get_object_or_404
from .forms import EmployerForm, JobForm
from django.contrib.auth.decorators import login_required
from .models import Job, Employer
from django.contrib import messages
from job.models import JobApplication
# Create your views here.

@login_required
def employer_profile(request):

    if request.method == "POST":
        form = EmployerForm(request.POST)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.user = request.user
            employer.save()
            return redirect('employer_dashboard')

    else:
        form = EmployerForm()
    return render(request, 'employer_profile.html', {'form': form})

@login_required
def employer_dashboard(request):
    employer = Employer.objects.filter(user=request.user).first()
    if employer:
        jobs = Job.objects.filter(employer=employer).order_by('-created_at')
    else:
        jobs=[]
    return render(request, 'employer_dashboard.html',context={'jobs':jobs})

@login_required
def post_job(request):
    employer = Employer.objects.filter(user=request.user).first()
    msg=''
    if not employer:
        messages.error(request, "You must create an employer profile before posting a job.")
        return redirect('employer_profile')
    if request.method == "POST":
        form = JobForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            msg='Job Posted Successfuly'
            return render(request,'post_job.html',{'msg':msg})
        else:
            print(form.errors)
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

@login_required
def employer_job_detail(request, id):
    print(id)
    job = get_object_or_404(Job, id=id)
    return render(request, 'employer_job_details.html', {'job': job})

@login_required
def edit_job(request, id):
    employer = Employer.objects.get(user=request.user)
    job = get_object_or_404(Job, id=id, employer=employer)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_job_details', id=job.id)
        else:
            print(form.errors)
    else:
        form = JobForm(instance=job)

    return render(request, 'edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, id):
    employer = Employer.objects.filter(user=request.user).first()
    job = get_object_or_404(Job, id=id, employer=employer)
    job.delete()
    return redirect('employer_dashboard') 

@login_required
def job_applications(request, id):
    job = Job.objects.get(id=id)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'job_applications.html', {
        'job': job,
        'applications': applications
    })

@login_required
def employer_job_search(request):
    keyword = request.GET.get('keyword')
    location = request.GET.get('location')
    employer = Employer.objects.get(user=request.user)
    # show only jobs posted by this employer
    jobs = Job.objects.filter(employer=employer)
    if keyword:
        jobs = jobs.filter(job_title__icontains=keyword)
    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'employer_dashboard.html', {'jobs': jobs})