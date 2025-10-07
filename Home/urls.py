# Can be thought of as a table of contents for the whole project , link url to specific view 
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import signup,index,about,post
from .forms import LoginForm

urlpatterns = [
    path('', index , name='index'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form = LoginForm), name='login'),
    path('about/', about, name='about'),
    path('post/', post, name='post'),
    
]
# we are using django built in views and using the form we created in forms.py