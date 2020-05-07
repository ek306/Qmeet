from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer
from .forms import StudentCreationForm, StudentCategoriesForm, EventCategoriesForm
from .models import Student, Event, StudentProfile, StudentCategories, EventCategories, StudentProfileYear
from django.core import serializers
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from . import serializers


class SignUp(generic.CreateView):
    form_class = StudentCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@login_required()
def studentprofile(request):
    form = StudentCategoriesForm()
    return render(request, 'qmeet/studentprofile.html', {'form': form})


@login_required()
def new_student_profile(request):
    user = request.user
    if request.method == 'POST':
        form = StudentCategoriesForm(request.POST)
        if form.is_valid():
            student = user
            bio = form.cleaned_data['bio']
            location = form.cleaned_data['location']
            course = form.cleaned_data['course']
            year = form.cleaned_data['year']
            student_profile = StudentProfile(student=student, course=course, bio=bio, location=location)  # , display_picture=display_picture)
            student_profile.save()
            for categories in form.cleaned_data['categories']:
                student_categories = StudentCategories(student_profile=student_profile, categories=categories)
                student_categories.save()
            student_profile_year = StudentProfileYear(student_profile=student_profile, year=year)
            student_profile_year.save()
            # display_picture = form.cleaned_data['display_picture']
            return HttpResponse("Profile created")

@login_required()
def index(request):
    return render(request, 'index.html')


@login_required
def createevent(request):
    temp = request.GET['event_id']
    form = EventCategoriesForm()
    return render(request, 'qmeet/createevent.html', {'form': form})


def new_event(request):
    user = request.user
    if request.method == "POST":
        form = EventCategoriesForm(request.POST)
        if form.is_valid():
            student = user
            title = form.cleaned_data['title']
            location = form.cleaned_data['location']
            start_date = request.POST['start-date']
            end_date = request.POST['end-date']
            capacity = form.cleaned_data['capacity']
            event = Event(host=student, title=title, location=location, start_date=start_date, end_date=end_date, capacity=capacity)
            event.save()
            for categories in form.cleaned_data['categories']:
                event_categories = EventCategories(event=event, categories=categories)
                event_categories.save()
            return HttpResponse("Event created, and event categories created")

@login_required()
def students(request):
    return render(request, 'qmeet/students.html')


@login_required()
def events(request):
    return render(request, 'qmeet/events.html')


class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer


@login_required()
def get_all_students(request):
    student_list = Student.objects.all().values()
    return JsonResponse({
        'students': list(student_list)
    })


@login_required()
def get_all_events(request):
    event_list = Event.objects.all().values()
    return JsonResponse({
        'events': list(event_list)
    })


@login_required()
def get_event(request):
    temp = request.GET['event_id']
    event = Event.objects.get(id=temp)
    context = {'event': event}
    return render(request, 'qmeet/getstudentprofile.html', context)

