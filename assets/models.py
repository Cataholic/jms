from django.db import models

class Asset(models.Model):
    OS_Choice = [
        ('C', 'CentOS'),
        ('U', 'Ubuntu'),
        ('D', 'Debian'),
        ('R', 'Redhat'),
        ('B', 'BSD'),
    ]
    hostname = models.CharField(unique=True, max_length=128, verbose_name='Hostname')
    ip = models.GenericIPAddressField(verbose_name='IP', unique=True)
    port = models.IntegerField(default=22, verbose_name='端口')
    username = models.CharField(max_length=20, verbose_name='管理用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    os = models.CharField(choices=OS_Choice, max_length=2, verbose_name='系统平台')
    is_active = models.BooleanField(default=True, verbose_name='激活')

    def __str__(self):
        return self.hostname