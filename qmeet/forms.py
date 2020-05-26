from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Event, Categories, StudentCategories, StudentProfile, AcademicYear, Module, CourseModules, Course


class StudentCreationForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control datetimepicker-input', 'placeholder': 'Email'})
    )
    date_of_birth = forms.CharField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2')


class StudentCategoriesForm(ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'})
    )

    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        queryset=Categories.objects.all()
    )

    display_picture = forms.ImageField(widget=forms.FileInput, required=False)

    year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StudentProfile
        fields = ['course', 'year', 'location', 'categories', 'display_picture']


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
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    # username = forms.CharField(required=False)
    categories = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Categories
        fields = ['username', 'categories']


class FilterEventsForm(ModelForm):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event name'})
    )
    categories = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Categories
        fields = ['title', 'categories']
