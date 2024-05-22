from django.shortcuts import render
from django.views import generic
from .models import Post
from django.contrib.auth.decorators import login_required




# Create your views here.


class PostList(generic.ListView):
#     model = Post

   queryset = Post.objects.all()
   template_name = "post_list.html"
 
