from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone

# class Post(models.Model):
    # sno=models.AutoField(primary_key=True)
    # title=models.CharField(max_length=255)
    # author=models.CharField(max_length=14)
    # slug=models.CharField(max_length=130)
    # views= models.IntegerField(default=0)
    # timeStamp=models.DateTimeField(blank=True)
    # content=models.TextField()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES= ( ('draft','Draft'),('published','Published'),
                      )
    sno=models.AutoField(primary_key=True)
    views= models.IntegerField(default=0)                  
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tags= TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                    args=[self.publish.year,
                          self.publish.month,
                          self.publish.day,
                          self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    # def __str__(self):
    #     return self.title + " by " + self.author

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)
    created =models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'  




# FOR COMMENTS
# class Comment(models.Model):
#     post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     body = models.TextField()
#     created =models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)

#     class Meta:
#         ordering = ('created',)

#     def __str__(self):
#         return f'Connect by {self.name} on {self.post}'   
    
