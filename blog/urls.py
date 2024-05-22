from . import views
from django.urls import path
import blog.views

import authentication.views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('upload/', blog.views.blog_and_photo_upload, name='blog_and_photo_upload'),
    path('photo/', blog.views.photos, name='photos'),   
]
