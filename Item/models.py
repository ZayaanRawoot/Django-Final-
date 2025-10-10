from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Categories"
        # this controls the display of the models in your admin 
    
    def __str__(self):
        # iterable tuple 
        ordering = ('name',)
        return self.name #this returns the name of the category 
    
class Item(models.Model):
    """Job details"""
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)#an index in db between item and user, related name to get all the items easily belonging to a specific user, ondelete - if user is deleted then all items will aslo be deleted 
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) #much longer than 255 characters, blank and null = true in case user does not want to provide decrisptions for the product
    # price = models.FloatField()
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)


    # Job Overview
    city_location = models.CharField(max_length=200, blank=True)
    vacancy = models.PositiveIntegerField(default=1)
    job_nature = models.CharField(max_length=50, blank=True)
    yearly_salary = models.CharField(max_length=100, blank=True)
    application_deadline = models.DateField(blank=True, null=True)
    is_sold = models.BooleanField(default=False) #marks if sold or not 
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE) #an index in db between item and user, related name to get all the items easily belonging to a specific user, ondelete - if user is deleted then all items will aslo be deleted 
    created_at = models.DateTimeField(auto_now_add=True) #when item was created, added automatically with autonowadd

    # pillow is a python library for handling images like resizing , saving them

    def __str__(self):
        # iterable tuple 
        # ordering = ('name',)
        # return self.name #this returns the name of the category 
        return f'{self.name} - {self.location}'