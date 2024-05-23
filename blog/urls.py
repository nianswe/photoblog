from . import views
from django.urls import path
import blog.views

import authentication.views

urlpatterns = [
    # path('', views.PostList.as_view(), name='post_list'),
    
    path('', blog.views.Blog, name='home'),
    path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'),
    path('blog/<int:blog_id>/edit', blog.views.edit_blog, name='edit_blog'),
    path('upload/', blog.views.blog_and_photo_upload, name='blog_and_photo_upload'),
    path('photo/', blog.views.photos, name='photos'),
    
       
]
