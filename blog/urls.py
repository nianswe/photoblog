from . import views
from django.urls import path
import blog.views

import authentication.views

urlpatterns = [
    # path('', views.PostList.as_view(), name='post_list'),
    
    path('', blog.views.blog, name='blog'),
    # path('', views.PostList.as_view(), name='blog'),
    path('<int:blog_id>', blog.views.view_blog, name='view_blog'),
    path('<int:blog_id>/edit', blog.views.edit_blog, name='edit_blog'),
    path('upload/', blog.views.blog_and_photo_upload, name='blog_create'),
    path('photo/', blog.views.photos, name='photo_view'),
    path('photo/upload/', blog.views.photo_upload, name='photo_upload'),
    path('photo/upload-multiple/', blog.views.create_multiple_photos, name='create_multiple_photos'),
    
    
       
]
