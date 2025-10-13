from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404
from .forms import JobApplicationForm, EditJobApplicationForm
from .models import Category, Job ,JobApplication
# Create your views here.

def job_list(request):
    query = request.GET.get('query', '')#we default this to be empty
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    job_type = request.GET.get('job_type')
    location = request.GET.get('location', '')

    jobs = Job.objects.filter(is_filled=False)

    if category_id and int(category_id) != 0:
        # if we selected a category
        jobs = jobs.filter(category_id = category_id)


    if query:
        jobs = jobs.filter(Q(name__icontains = query) | Q(description__icontains = query))# i = insensitive . if the name contains the query , then the query will be processed. we use a py pair - so if the title or description contains it, it will search.

    if job_type:
        jobs = jobs.filter(job_nature__in = job_type)# i = insensitive . if the name contains the query , then the query will be processed. we use a py pair - so if the title or description contains it, it will search.
    
    if location:
        jobs = jobs.filter(location__icontains = location)

    job_types = ["Full Time", "Part Time", "Remote", "Freelance"]

    context = {
        'jobs':jobs,
        'query': query,
        'categories':categories,
        'category_id': int(category_id),
        'selected_job_types': job_type,
        'location': location

    }

    return render(request, 'job/job_list.html', context)

def job_detail(request, pk):
    """View for job details"""
    job = get_object_or_404(Job, pk=pk) #gives error if object doesnt exist in db. gets job from job model where the pk is the pk on the model itself 
    related_items = Job.objects.filter(category= job.category, is_filled=False).exclude(pk=pk)[0:3] #fetch 3 related jobs excluding the current one.
    return render(request, 'job/job_detail.html', {'job':job, 'related_items': related_items} )

# @login_required
def apply(request, pk):
    job = get_object_or_404(Job, pk=pk) #gives error if object doesnt exist in db. gets job from job model where the pk is the pk on the model itself 

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.job = job
            form.save()
            return redirect('success')

            # return redirect('job:job_detail', pk = job.id ) #pass in detail view and id/pk of the job we just created 
    else:
        form = JobApplicationForm()

    return render(request,'job/application_form.html', {'form':form, 'title':f'Apply for {job.name}'})

# @login_required
def edit(request,pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        form = EditJobApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
           
            form.save()# we can just say form.save because the created by is already set

            return redirect('job:job_detail', pk =application.job.pk ) #pass in detail view and id/pk of the job we just created 
    else:
        form = EditJobApplicationForm(instance=application)#instance passes in some data so the form wont be empty, we do the sane for form variable here

    return render(request,'job/application_form.html', {'form':form, 'title':f'Edit Application'})


# @login_required
def delete(request, pk):
    application = get_object_or_404(JobApplication, pk=pk) #we dont want to get objects you havent created yourself 
    application.delete()
    return redirect('dashboard:index')#redirect the user to the dashboard



def applied(request):
        return render(request,'job/applied.html')
