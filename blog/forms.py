from django import forms

from . import models

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'caption']
        
class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'slug', 'body', 'status', 'pubstatus', ]