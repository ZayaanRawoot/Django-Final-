# Can be thought of as a table of contents for the whole project , link url to specific view 
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views 
from .forms import LoginForm
app_name = 'core'
urlpatterns = [
    path('', views.index , name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form = LoginForm), name='login')
]
# we are using django built in views and using the form we created in forms.py