from django.urls import path 
from . import views 

# this will now be a name space for this app
app_name= 'Job'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    # path('new/', views.new, name='new'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('job/<int:pk>/apply/', views.apply, name='apply'),

    # when this has an ineteger , we want to use the details view and the name will be detail 
    path('application/<int:pk>/delete/', views.delete, name='delete'),
    path('application/<int:pk>/edit/', views.edit, name='edit'),
    path('applied/', views.applied, name='applied'),

]

