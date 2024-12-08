# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None
    fullname = models.CharField(max_length=254, null=True)
    national_code = models.CharField(max_length=15, unique=True)
    student_number = models.CharField(max_length=15, unique=True, null=False)
    email = models.EmailField(max_length=254, unique=True)
    department = models.CharField(max_length=254, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return (self.fullname + " " + self.national_code)
