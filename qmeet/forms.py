from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime
from .models import Student, Categories, StudentCategories


class StudentCreationForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ('username', 'email', 'date_of_birth')


class StudentCategoriesForm(ModelForm):
    bio = forms.CharField(widget=forms.Textarea)
    location = forms.CharField()
    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Categories.objects.all()
    )

    class Meta:
        model = StudentCategories
        fields = ['bio', 'location', 'categories']
