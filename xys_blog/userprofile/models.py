from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class XysUser(User):
    security_register_key = models.CharField(max_length=100)
