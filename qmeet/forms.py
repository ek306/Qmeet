from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime
from .models import Student


class StudentCreationForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ('username', 'email', 'date_of_birth')