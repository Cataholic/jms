from django.db import models

from django.conf import settings
from assets.models import Assets


class Perm(models.Model):
    name = models.CharField(max_length=64, verbose_name='名称')
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='用户')
    asset = models.ManyToManyField(Assets, verbose_name='资产')
    date_add = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.id