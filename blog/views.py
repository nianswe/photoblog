from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from . import forms, models 
from django.contrib.auth.decorators import login_required


# Create your views here.



@login_required
def photos(request):
    photos = models.Photo.objects.all()
    return render(request, 'blog/photos.html', context={'photos': photos})
   
   
def blog_and_photo_upload(request):
      blog_form = forms.BlogForm()
      photo_form = forms.PhotoForm()
      if request.method == 'POST':
         blog_form = forms.BlogForm(request.POST)
         photo_form = forms.PhotoForm(request.POST, request.FILES)
         if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            return redirect('post_list')
      context = {
         'blog_form': blog_form,
         'photo_form': photo_form,
      }
      return render(request, 'blog/add_blog_post.html', context=context)

 
class PostList(generic.ListView):
#     model = Post

   queryset = Post.objects.all()
   template_name = "post_list.html"
 
