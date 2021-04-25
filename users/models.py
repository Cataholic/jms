from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=32, help_text='昵称')
    wechat = models.CharField(max_length=64)

    def __str__(self):
        return self.name