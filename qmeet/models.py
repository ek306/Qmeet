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
    # image = models.ImageField(upload_to='event_images', blank=True)

    def __str__(self):
        return self.title


class Categories(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class EventCategories(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)


class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.TextField(max_length=30, blank=True)
    #display_picture = models.ImageField(upload_to='profile_images', blank=True)


class StudentCategories(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
