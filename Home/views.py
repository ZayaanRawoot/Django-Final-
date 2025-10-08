from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from Dashboard.models import Job

# Home Page View
def index(request):
    # Show latest 6 jobs that are not sold, ordered by date posted descending
    jobs = Job.objects.all().order_by('-date_posted')[:6]
    return render(request, 'index.html', {
        'jobs': jobs,
    })

# Job Detail Page
def detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'item:job_detail', {'job': job})

# Signup Page
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('home:index')

# About Page
def about(request):
    return render(request, 'about.html')

# Redirects for dashboard/post
@login_required
def post(request):
    return redirect('dashboard:create')  # Use URL names for safety

@login_required
def dashboard(request):
    return redirect('dashboard:overview')
