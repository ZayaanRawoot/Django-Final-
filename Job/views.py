from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404
from .forms import JobApplicationForm, EditJobApplicationForm
from .models import Category, Job ,JobApplication
# Create your views here.

def job_list(request):
    query = request.GET.get('query', '')#we default this to be empty
    category_id = request.GET.get('category', '')

    try:
        category_id = int(category_id)
    except(ValueError,TypeError):
        category_id = 0
    
    categories = Category.objects.all()
    jobs = Job.objects.filter(is_filled=False)

    if category_id:
        # if we selected a category
        jobs = jobs.filter(category_id = category_id)


    if query:
        jobs = jobs.filter(Q(name__icontains = query) | Q(description__icontains = query))# i = insensitive . if the name contains the query , then the query will be processed. we use a py pair - so if the title or description contains it, it will search.

 # get selected job types from checkboxes.returns a list of checkbox values
    selected_job_types = request.GET.getlist('job_type')
    if selected_job_types:
        jobs = jobs.filter(job_nature__in=selected_job_types)

    print("Selected job types:", selected_job_types)


    return render(request, 'job/job_list.html', {'jobs':jobs, 'query': query, 'categories':
    categories, 'category_id': int(category_id),'selected_job_types':selected_job_types}) #pass to template checkbox states

def job_detail(request, pk):
    """View for job details"""
    job = get_object_or_404(Job, pk=pk) #gives error if object doesnt exist in db. gets job from job model where the pk is the pk on the model itself 
    related_items = Job.objects.filter(category= job.category, is_filled=False).exclude(pk=pk)[0:3] #fetch 3 related jobs excluding the current one.
    return render(request, 'job/job_detail.html', {'job':job, 'related_items': related_items} )

# @login_required
def apply(request, pk):
    # Get the job or return 404 if not found
    job = get_object_or_404(Job, pk=pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job  # assign the job
            try:
                application.save()
                messages.success(request, 'Your application has been submitted!')
                return redirect('job_list')  # change to your jobs list URL
            except Exception as e:
                messages.error(request, f'Error saving application: {e}')
        else:
            # Print form errors in console (helpful for debugging)
            print(form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm()

    return render(request, 'job/application_form.html', {
        'form': form,
        'title': f'Apply for {job.name}',
        'job': job
    })

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
