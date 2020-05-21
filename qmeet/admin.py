from django.contrib import admin
from .models import Student, Event, Categories, StudentCategories, StudentEvents, EventCategories, StudentProfile, Course, CourseModules, Department, Module, AcademicYear, StudentProfileYear, FriendRequest

admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Categories)
admin.site.register(StudentCategories)
admin.site.register(StudentEvents)
admin.site.register(EventCategories)
admin.site.register(StudentProfile)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Module)
admin.site.register(CourseModules)
admin.site.register(AcademicYear)
admin.site.register(StudentProfileYear)
admin.site.register(FriendRequest)