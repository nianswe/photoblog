from . import views
from django.urls import path
import home.views
from home import views as index_views

import authentication.views

urlpatterns = [
    # path('', views.PostList.as_view(), name='post_list'),
    
    path('', home.views.photo_home, name='photos'),
]
    
    