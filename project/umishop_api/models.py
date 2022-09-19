from django.db import models


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    objects = models.Manager()
