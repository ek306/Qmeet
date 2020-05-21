from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from .models import Student, Event, Categories, StudentCategories, StudentProfile, AcademicYear, Module, CourseModules


class StudentCreationForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')


class StudentCategoriesForm(ModelForm):
    #bio = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(widget=forms.TextInput)
    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Categories.objects.all()
    )
    year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all()
    )
    #display_picture = forms.ImageField(required=False)

    class Meta:
        model = StudentProfile
        fields = ['course', 'year', 'location', 'categories']  # , 'display_picture']


class EventCategoriesForm(ModelForm):
    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Event
        fields = ['title', 'location', 'capacity', 'categories']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class', 'form-control'})
        }

class FilterStudentsForm(ModelForm):
    username = forms.CharField(required=False)
    categories = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Categories
        fields = ['username', 'categories']


class FilterEventsForm(ModelForm):
    title = forms.CharField(required=False)
    categories = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Categories
        fields = ['title', 'categories']
