from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from Item.models import Item
# Create your views here.

@login_required
def index(request):
    items = Item.objects.filter(created_by = request.user) # this returns all items created by the user who is currently signed in 
    return render(request, '/index.html', {'items': items, })

