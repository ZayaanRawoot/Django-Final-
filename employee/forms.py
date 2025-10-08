from django import forms 
from .models import Employee

class EmployeeForm(forms.ModelForm):
    # created nested class called meta 
    class Meta:
        model = Employee
        # 2 ways to write fields for each field in model , in tuple etc you do this when you want specific fields in your model - but in this case we require all fields based on structure : this retrieves all fields for the form 
        fields = '__all__'