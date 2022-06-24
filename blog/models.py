from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.

def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)
    
class Post(models.Model):
    
    #automatically filters out posts that aren't published
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published') 
    
    class Meta:
        ordering = ('-published',)
    
    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    
    #data fields
    title = models.CharField(max_length=250)
    image = models.ImageField(_("Image"), upload_to=upload_to, default='rango.jpg')
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(
        max_length=10, choices=options, default='published')
    
    #activity functionality
    activity_start = models.DateTimeField(default=timezone.now)
    activity_end = models.DateTimeField(default=timezone.now)
    activity_distance = models.FloatField(default=0.0)
    DISTANCE_CHOICES = (
        ("km", "Kilometers"),
        ("mi", "Miles"),
    )
    distance_units = models.CharField(
        max_length=10, choices = DISTANCE_CHOICES, default="mi"
    )
    ACTIVITY_CHOICES = (
        ("Running", "Running"),
        ("Biking", "Biking"),
        ("Swimming", "Swimming"),
    )
    activity_type = models.CharField(
        max_length=8, choices=ACTIVITY_CHOICES, default="running")
    
    objects = models.Manager()
    postobjects = PostObjects()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    
    class Meta:
        ordering = ('-published',)
        
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author') 
    parent_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comment_post')
    content = models.TextField()
    
    objects = models.Manager()
    
    def __str__(self):
        return 'Re: %s - %s: %s' % (self.parent_post.title, self.author.user_name, self.published)