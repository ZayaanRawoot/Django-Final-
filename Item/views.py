from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404
from .forms import NewItemForm, EditItemForm
from .models import Category,Item
# Create your views here.

def items(request):
    query = request.GET.get('query', '')#we default this to be empty
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        # if we selected a category
        items = items.filter(category_id = category_id)


    if query:
        items = items.filter(Q(name__icontains = query) | Q(description__icontains = query))# i = insensitive . if the name contains the query , then the query will be processed. we use a py pair - so if the title or description contains it, it will search.

    return render(request, 'item/items.html', {'items':items, 'query': query, 'categories':
    categories, 'category_id': int(category_id)})

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk) #gives error if object doesnt exist in db. gets item from item model where the pk is the pk on the model itself 
    related_items = Item.objects.filter(category= item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'item/detail.html', {'item':item, 'related_items': related_items} )

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)#this will create an object but not save it to the database. the row will have an error otherwise if it is saved without the created_by field 
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk = item.id ) #pass in detail view and id/pk of the item we just created 
    else:
        form = NewItemForm()

    return render(request,'item/form.html', {'form':form, 'title':'New Item'})

@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
           
            form.save()# we can just say form.save because the created by is already set

            return redirect('item:detail', pk = item.id ) #pass in detail view and id/pk of the item we just created 
    else:
        form = EditItemForm(instance=item)#instance passes in some data so the form wont be empty, we do the sane for form variable here

    return render(request,'item/form.html', {'form':form, 'title':'Edit Item'})


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user) #we dont want to get objects you havent created yourself 
    item.delete()
    return redirect('dashboard:index')#redirect the user to the dashboard