from django.contrib import admin
from .models import Student, Event, Categories, StudentCategories, EventCategories, StudentProfile

admin.site.register(Student)

admin.site.register(Event)

admin.site.register(Categories)

admin.site.register(StudentCategories)

admin.site.register(EventCategories)

admin.site.register(StudentProfile)
