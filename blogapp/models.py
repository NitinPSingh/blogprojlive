from django.db import models
from django.urls import reverse # new
from django.contrib.auth.models import AbstractUser,User
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey( 'auth.User', on_delete=models.CASCADE, )
    head_image = models.ImageField(blank=False,upload_to='blogimage/',null=True)
    body = RichTextField(blank=True,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name='blog_post')
    def like_count(self):
        return self.likes.count()
    def __str__(self):
        return self.title
    def get_absolute_url(self): # new
        return reverse('post_detail', args=[str(self.id)])
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)


class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True,null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username




class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE,)
    author = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
            )
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)




    def __str__(self):
        return self.text
