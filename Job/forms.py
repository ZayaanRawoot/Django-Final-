from django import forms 
from .models import JobApplication

# because we want to apply the same styling throughout the form we create this variable :
INPUT_CLASSES =  'form-control mb-3'

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ( 'full_name', 'email', 'phone', 'motivational', 'curriculum_vitae')

        widgets = {
            'job':forms.HiddenInput(),
            'full_name':forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your full name'}),
            'email':forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your email'}),
            'motivational':forms.Textarea(attrs={'class': INPUT_CLASSES, 'placeholder': 'Write here', 'rows':4,}),
            'phone':forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your phone number'}),
            'curriculum_vitae':forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload CV'}),
        }

    def clean_curriculum_vitae(self):
        cv = self.cleaned_data.get('curriculum_vitae')
        if cv:
            if cv.size > 5*1024*1024:
                raise forms.ValidationError("CV file too large (max 5MB).")
            if not cv.name.endswith(('.pdf', '.doc', '.docx')):
                raise forms.ValidationError("CV must be a PDF or Word document.")
        return cv

class EditJobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ( 'job', 'full_name', 'email', 'phone', 'motivational', 'curriculum_vitae')

        widgets = {
            'job':forms.HiddenInput(),
            'full_name':forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your full name'}),
            'email':forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your email'}),
            'motivational':forms.Textarea(attrs={'class': INPUT_CLASSES, 'placeholder': 'Write here'}),
            'phone':forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your phone number'}),
            'curriculum_vitae':forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload CV'}),
        }