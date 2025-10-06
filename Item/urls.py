from django.urls import path 
from . import views 

# this will now be a name space for this app
urlpatterns = [
    path('', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    # when this has an ineteger , we want to use the details view and the name will be detail 
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
]
