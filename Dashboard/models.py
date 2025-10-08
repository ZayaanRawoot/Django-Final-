from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Job(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tech'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]

    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('freelance', 'Freelance'),
        ('remote', 'Remote'),
        ('internship', 'Internship'),
    ]

    job_position = models.CharField(max_length=255)
    description = models.TextField(max_length=600)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_posted = models.DateField(auto_now_add=True)
    company_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # NEW
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='full-time')  # NEW
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.job_position} at {self.company_name}"
    
    
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    cv = models.FileField(
        upload_to='cvs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    date_applied = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')  # Prevent duplicate applications

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job}"
