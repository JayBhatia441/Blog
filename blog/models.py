from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ckeditor.fields import RichTextField

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name





class Blog(models.Model):
    title = models.CharField(max_length = 20)

    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    header_image = models.ImageField(blank=True,null=True,upload_to="images/")


    text = RichTextField(blank=True,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)
    likes_jay = models.ManyToManyField(User,related_name='jay_likes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def approve_comments(self):
        self.comment.filter(approved_comment=True)

    def countlikes(self):
        return self.likes_jay.count()

class Comment(models.Model):

    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comment')
    author = models.CharField(max_length=20)
    text = models.TextField(blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    aprroved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.author
    def approve(self):
        self.approved_comment=True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:list')

class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField()
    header_image = models.ImageField(blank=True,null=True,upload_to="images/profile")
    website_url = models.CharField(max_length = 200,null=True,blank=True)
    facebook_url = models.CharField(max_length = 200,null=True,blank=True)
    twitter_url = models.CharField(max_length = 200,null=True,blank=True)
    instagram_url = models.CharField(max_length = 200,null=True,blank=True)





    def __str__(self):
        return self.user.username

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)
