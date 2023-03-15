from django.db import models

# Create your models here.
class User(models.Model):
    id = models.Index
    name = models.CharField("用户名", max_length=50, default='')
    password = models.CharField("密码", max_length=255, default='')