from django.contrib import admin
from .models import Category, Job, JobApplication 
# import models
# Register your models here.
from django.utils.html import format_html

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'job', 'curriculum_vitae_link', 'created_at')

    def curriculum_vitae_link(self, obj):
        if obj.curriculum_vitae:
            return format_html('<a href="{}" target="_blank">View CV</a>', obj.curriculum_vitae.url)
        return "-"
    curriculum_vitae_link.short_description = "CV"


admin.site.register(Category)
admin.site.register(Job)
admin.site.register(JobApplication,JobApplicationAdmin)