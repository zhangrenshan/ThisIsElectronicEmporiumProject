from django.db import models


class LoginUser(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=18)

    username = models.CharField(max_length=32)
    phoneNumber = models.CharField(max_length=11, null=True, blank=True)
    photo = models.ImageField(upload_to='images', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=32, null=True, blank=True)
    address = models.TextField(max_length=254, null=True, blank=True)
# Create your models here.
