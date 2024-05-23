from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Blog
from . import forms, models
from django.views.generic import ListView 
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
            return redirect('home')
      context = {
         'blog_form': blog_form,
         'photo_form': photo_form,
      }
      return render(request, 'blog/add_blog_post.html', context=context)



@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})
 

 
@login_required 
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    edit_form = forms.BlogForm(instance=blog)
    edit_photo_form = forms.PhotoForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        if 'edit_blog' in request.POST:
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        
        if 'edit_photo' in request.POST:
            edit_photo_form = forms.PhotoForm(request.POST)
            if edit_photo_form.is_valid():
                edit_photo_form.save()
                return redirect('home')
        
        if 'delete_blog' in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_blog.html', {context:context})


 
class PostList(ListView):
    """
    Alternative post list view
    """
    queryset = Blog.published.filter(status=Blog.Status.PUBLISHED)
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post_list.html'
 
