from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        # this controls the display of the models in your admin
        verbose_name_plural = "Categories"
        # iterable tuple 
        ordering = ('name',)
 
    
    def __str__(self):  
        return self.name #this returns the name of the category 


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField(blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    comany_description = models.TextField(blank=True, null=True) #much longer than 255 characters, blank and null = true in case user does not want to provide decrisptions for the product
   
    
class Job(models.Model):
    """Job details"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='jobs', on_delete=models.CASCADE)#an index in db between item and user, related name to get all the items easily belonging to a specific user, ondelete - if user is deleted then all items will aslo be deleted 
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) #much longer than 255 characters, blank and null = true in case user does not want to provide decrisptions for the product
    # price = models.FloatField()
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True)



    # Job Overview
    city_location = models.CharField(max_length=200, blank=True)
    vacancy = models.PositiveIntegerField(default=1)
    job_nature = models.CharField(max_length=50, blank=True)
    yearly_salary = models.CharField(max_length=100, blank=True)
    application_deadline = models.DateField(blank=True, null=True)
    is_filled = models.BooleanField(default=False) #marks if sold or not 
    created_by = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE) #an index in db between item and user, related name to get all the items easily belonging to a specific user, ondelete - if user is deleted then all items will aslo be deleted 
    created_at = models.DateTimeField(auto_now_add=True) #when item was created, added automatically with autonowadd

    # Skills & Experience
    skills = models.TextField(blank=True, null=True, help_text ="Comma-seperated list of skills")
    experience = models.TextField(blank=True, null=True, help_text ="Comma-seperated list of skills")


    def __str__(self):
        # iterable tuple 
        # ordering = ('name',)
        # return self.name #this returns the name of the category 
        return f'{self.name} - {self.location}'

    def skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
        
    def experience_list(self):
        if self.experience:
            return [exp.strip() for exp in self.experience.split(',')]
        return []

    class Meta:
        # this controls the display of the models in your admin
        ordering = ['-created_at',]
 


class JobApplication(models.Model):
    """Job aplication form"""
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    motivational = models.CharField(max_length=255)
    curriculum_vitae = models.FileField(upload_to ='cv/')
    job = models.ForeignKey('Job', on_delete=models.CASCADE,related_name='applications')
    created_at = models.DateTimeField(auto_now_add=True) #when item was created, added automatically with autonowadd

    class Meta:
        """user should not apply multiple times to the same job"""
        unique_together = ('email', 'job')
        ordering = ['-created_at',]

    def __str__(self):
        # ordering = ('name',)
        # return self.name #this returns the name of the category 
        return f'{self.full_name} ({self.email}) - {self.job.name}'

