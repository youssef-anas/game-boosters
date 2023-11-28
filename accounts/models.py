from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
# models.py

class UserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)



class BaseUser(AbstractUser):
    phone_number = PhoneNumberField(null=True,blank=True)
    email_verified_at = models.DateTimeField(null=True,blank=True)
    image = models.ImageField(upload_to='media/accounts/',blank=True,null=True)
    country = CountryField(blank=True,null=True)
    about_you = models.TextField(max_length=1000,null=True, blank=True)
    
