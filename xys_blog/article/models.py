from django.db import models
from django import forms
# Create your models here.
# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone


# BlogArticle文章类
class BlogArticle(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    abstract = models.CharField(max_length=1024)
    body = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = ('title', 'body', 'category')
