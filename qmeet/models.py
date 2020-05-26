from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager, BaseUserManager, PermissionsMixin


class Department(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.TextField()
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.TextField()
    code = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name


class CourseModules(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        course_name = str(self.course)
        module_name = str(self.module)
        return course_name + ' - ' + module_name


class Student(AbstractUser):
    pass
    # add additional fields in here
    date_of_birth = models.DateField(null=True, default='2000-01-01')

    def __str__(self):
        return self.username


class Event(models.Model):
    host = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    capacity = models.IntegerField(default=100)
    attendees = models.ManyToManyField(Student, blank=True, related_name="attendees")
    # image = models.ImageField(upload_to='event_images', blank=True)

    def __str__(self):
        return self.title


class Categories(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class StudentEvents(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        student = str(self.student)
        event = str(self.event)
        return student + ' - ' + event


class EventCategories(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        event = str(self.event)
        categories = str(self.categories)
        return event + ' - ' + categories


class AcademicYear(models.Model):
    year = models.CharField(max_length=20)

    def __str__(self):
        return self.year


class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.TextField(max_length=30, blank=True)
    friends = models.ManyToManyField("StudentProfile", blank=True)
    display_picture = models.ImageField(upload_to='images/', blank=True, default='default-avatar.jpg')

    def __str__(self):
        return self.student.username


class FriendRequest(models.Model):
    to_user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='from_user')

    def __str__(self):
        to_user = str(self.to_user)
        from_user = str(self.from_user)
        return 'from ' + from_user + ' to ' + to_user


class StudentCategories(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        student_profile = str(self.student_profile)
        categories = str(self.categories)
        return student_profile + ' - ' + categories


class StudentProfileYear(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        student_profile = str(self.student_profile)
        year = str(self.year)
        return student_profile + year


class Semester(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name}"


class SemesterModule(models.Model):
    start_hour = models.IntegerField(default=0)
    end_hour = models.IntegerField(default=0)
    day = models.CharField(max_length=9)
    abbreviated_day = models.CharField(max_length=3)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    @property
    def duration(self):
        return self.end_hour - self.start_hour

    def __str__(self):
        return f"{self.module.name} {self.semester.name}"


class GetTimetableForUser(models.Model):
    semester_name = models.CharField(max_length=20)
    module_name = models.CharField(max_length=50)
    start_hour = models.IntegerField
    end_hour = models.IntegerField
    abbreviated_day = models.CharField(max_length=3)
    duration = models.IntegerField


class SelectedCategories(models.Model):
    categories = models.CharField(primary_key=True, max_length=255)
