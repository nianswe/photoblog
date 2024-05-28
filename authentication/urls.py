from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
import authentication.views

# # Login/Log out/Sign up - Credit and insperation: https://openclassrooms.com/
urlpatterns = [
    path('', LoginView.as_view(
           template_name='authentication/login.html',
           redirect_authenticated_user=True),
        name='login'),
   path('logout/', authentication.views.logout_user, name='logout'),
   path('signup/', authentication.views.signup_page, name='signup'),
   
       
]