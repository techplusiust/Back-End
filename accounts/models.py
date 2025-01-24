from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model without a username or is_staff field.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    is_staff = None

    fullname = models.CharField(max_length=254, null=True)
    national_code = models.CharField(max_length=15, unique=True)
    student_number = models.CharField(max_length=15, unique=True, null=False)
    email = models.EmailField(max_length=254, unique=True)
    department = models.CharField(max_length=254, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.fullname} ({self.email})"
