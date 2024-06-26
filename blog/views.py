from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Blog
from . import forms, models
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.contrib.auth.models import User


@login_required
def blog(request):
    photos = models.Photo.objects.all()
    blogs = models.Blog.objects.order_by('-publish')
    return render(request, 'blog/post_list.html',
                  context={'photos': photos, 'blogs': blogs})


@login_required
def photos(request):
    photos = models.Photo.objects.order_by('-date_created')
    return render(request, 'blog/photos.html', context={'photos': photos})


@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})


@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form': form})


@login_required
def create_multiple_photos(request):
    PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormSet()
    if request.method == 'POST':
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
    return render(request,
                  'blog/create_multiple_photos.html',
                  {'formset': formset})


@login_required
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
    # delete_form = forms.DeleteBlogForm()

    if request.user == blog.author:
        if request.method == 'POST':
            if 'edit_blog' in request.POST:
                edit_form = forms.BlogForm(request.POST, instance=blog)
                if edit_form.is_valid():
                    edit_form.save()
                    return redirect('home')

            # if 'delete_blog' in request.POST:
            #    delete_form = forms.DeleteBlogForm(request.POST)
            #    if delete_form.is_valid():
            #        blog.delete()
            #        return redirect('home')
        context = {
            'edit_form': edit_form,
            # 'delete_form': delete_form,
        }
        return render(request,
                      'blog/edit_blog.html',
                      context=context)
        
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    delete_form = forms.DeleteBlogForm()

    if request.user == blog.author:
        if request.method == 'POST':
            if 'delete_blog' in request.POST:
                delete_form = forms.DeleteBlogForm(request.POST)
                if delete_form.is_valid():
                    blog.delete()
                    return redirect('home')
        context = {
            'delete_form': delete_form,
        }
        return render(request,
                      'blog/delete_blog.html',
                      context=context)


class PostList(ListView):
    """
    Alternative post list view
    """
    queryset = Blog.published.filter(status=Blog.Status.PUBLISHED)
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post_list.html'
