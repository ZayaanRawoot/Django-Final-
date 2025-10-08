from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobForm
from .models import Job, Application

# This is to post a job
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('dashboard:list')  # This should match the URL name
    else:
        form = JobForm()
    return render(request, 'dashboard/post_job.html', {'form': form})

# Update a job
@login_required
def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('dashboard:overview')
    else:
        form = JobForm(instance=job)
    return render(request, 'dashboard/update.html', {'form': form})

# Delete a job
@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('dashboard:list')
    return HttpResponseNotAllowed(['POST'])

# Show jobs created by current user
@login_required
def my_jobs_view(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'dashboard/list.html', {'jobs': jobs})

# View to see who applied to your posted jobs
@login_required
def view_applicants_to_my_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)
    applications = Application.objects.filter(job__in=jobs).select_related('job', 'applicant')
    return render(request, 'dashboard/applicants.html', {'applications': applications})

# View to see which jobs the user applied to
@login_required
def jobs_user_applied_to(request):
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'dashboard/applied_jobs.html', {'applications': applications})

# Dashboard overview combining all tables
@login_required
def dashboard_overview(request):
    my_jobs = Job.objects.filter(posted_by=request.user)
    applicants = Application.objects.filter(job__in=my_jobs).select_related('job', 'applicant')
    applied_jobs = Application.objects.filter(applicant=request.user).select_related('job')

    context = {
        'my_jobs': my_jobs,
        'applicants': applicants,
        'applied_jobs': applied_jobs,
    }
    return render(request, 'dashboard/overview.html', context)

# New: Delete an application the user made
@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    if request.method == 'POST':
        application.delete()
        return redirect('dashboard:overview')
    return HttpResponseNotAllowed(['POST'])
