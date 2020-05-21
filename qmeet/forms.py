from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime
from .models import Student, Event, Categories, StudentCategories, StudentProfile, AcademicYear, Module, CourseModules


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
    year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all()
    )

    class Meta:
        model = StudentProfile
        fields = ['course', 'year', 'bio', 'location', 'categories']


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

# class ModulesForm(ModelForm):
#    module_one = forms.ModelChoiceField(
#        queryset=Module.objects.all()
#    )

#    def __init__(self, *args, **kwargs):
#        user = kwargs.pop('user', None)
#        super(ModulesForm, self).__init__(*args, **kwargs)
#        if user is not None:
#            self.fields['module_one'].queryset = Module.objects.filter(course = user.StudentProfile.course)
