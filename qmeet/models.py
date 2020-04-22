from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager, BaseUserManager, PermissionsMixin


class Student(AbstractUser):
    pass
    # add additional fields in here
    date_of_birth = models.DateField(null=True, default='2000-01-01')

    def __str__(self):
        return self.username


class Event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    capacity = models.IntegerField(default=100)
    #image = models.ImageField(upload_to='event_images', blank=True)

    def __str__(self):
        return self.title
