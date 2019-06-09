from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from slugify import slugify
# Register your models here.


class Image(models.Model):
    title = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to=settings.IMAGE_PREFIX, default='/tmp/none.jpg')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images", null=True)
    url = models.URLField(default="")
    slug = models.SlugField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='images/%Y/%m/%d')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
