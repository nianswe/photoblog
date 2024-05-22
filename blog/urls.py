from . import views
from django.urls import path
import blog.views

import authentication.views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    
    
    
]
