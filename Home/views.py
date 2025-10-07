from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# Where we define views for the app - our logic to respond and display certain things/pages 
# Create your views here.
from Item.models import Category, Item
from .forms import SignUpForm

app_name = 'Home'

def index(request):
    # request is info about the browser ,ip address, if its a GET, POST request etc. has to be put on all views we use
    items = Item.objects.filter(is_sold=False)[0:6] # if it is not sold it will display 6 latest items 
    categories = Category.objects.all() #gets all categories
    return render(request, 'index.html', {'categories':categories, 'items':items}) #returns core/index.html to display, the dictionary is also a list of items that can be iterated over 


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login/')
    else:
        # create instance of the form and return render the template 
         form = SignUpForm()


    return render(request, 'signup.html', {'form':form})

def about(request):
    return render(request, 'about.html')

@login_required
def post(request):
    return redirect('item:create')