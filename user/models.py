from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('seller', 'seller'),
        ('client', 'client')
    )
    phone = models.CharField(max_length=9, validators=[MinLengthValidator(9), MaxLengthValidator(9)], unique=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=50, blank=True, null=True, choices=ROLE_CHOICES, default="client")

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name_plural = 'Users'
