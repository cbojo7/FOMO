from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(models.Model):
    
    salary = models.CharField(max_length=255, blank=True)
    birthday = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=15, blank=True)

