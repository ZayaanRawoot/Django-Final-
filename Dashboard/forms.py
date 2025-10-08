from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=Job.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'style': 'max-width: 450px; margin-bottom: 15px;'})
    )
    job_type = forms.ChoiceField(
        choices=Job.JOB_TYPE_CHOICES,
        widget=forms.Select(attrs={'style': 'max-width: 450px; margin-bottom: 15px;'})
    )

    class Meta:
        model = Job
        fields = ['job_position', 'company_name', 'description', 'salary', 'category', 'job_type']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name', 'style': 'max-width: 450px; margin-bottom: 15px;'}),
            'job_position': forms.TextInput(attrs={'placeholder': 'Position Name', 'style': 'max-width: 450px; margin-bottom: 15px;'}),
            'description': forms.Textarea(attrs={'placeholder': 'Job Description', 'style': 'max-width: 450px; margin-bottom: 15px;'}),
            'salary': forms.NumberInput(attrs={'placeholder': 'Salary per month', 'style': 'max-width: 450px; margin-bottom: 15px;'}),
        }
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'cv']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
