from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from PIL import Image
from cloudinary.models import CloudinaryField


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                    .filter(status=Blog.Status.PUBLISHED)

class PhotoPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                    .filter(status=Photo.Status.PUBLISHED)


class Photo(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    
    class PubStatus(models.TextChoices):
        PRIVATE = 'PR', 'Private'
        SHARED = 'SH', 'Shared'
    
    
    # image = models.ImageField()
    image = CloudinaryField('image', default='placeholder')
    slug = AutoSlugField(populate_from='image', unique=True)
    id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=128, null=False, blank=False)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    published = PhotoPublishedManager()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)
    pubstatus = models.CharField(max_length=2, choices=PubStatus.choices, default=PubStatus.PRIVATE)
    
    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # save the resized image to the file system
        # this is not the model save method!
        image.save(self.image.path)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
        
    def __str__(self):
        return self.caption + ' (' + self.pubstatus + ')'


class Blog(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    
    class Photo(models.TextChoices):
        PRIVATE = 'PR', 'Private'
        SHARED = 'SH', 'Shared'    
    
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True)
    
    author = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='blog_posts')
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    eventdate = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
        choices=Status.choices,
        default=Status.PUBLISHED)
    pubstatus = models.CharField(max_length=2,
        choices=PubStatus.choices,
        default=PubStatus.PRIVATE)
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #    return reverse('private_blog:post_detail',
    #                   args=[self.publish.year,
    #                        self.publish.month,
    #                        self.publish.day,
    #                        self.slug])
    