from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer
from .forms import StudentCreationForm, StudentCategoriesForm
from .models import Student, Event, StudentProfile, StudentCategories
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
            student_profile = StudentProfile(student=student, bio=bio, location=location)  # , display_picture=display_picture)
            student_profile.save()
            for categories in form.cleaned_data['categories']:
                student_categories = StudentCategories(student_profile=student_profile, categories=categories)
                student_categories.save()
            #display_picture = form.cleaned_data['display_picture']
            return HttpResponse("Profile created")

@login_required()
def index(request):
    return render(request, 'index.html')


@login_required
def createevent(request):
    return render(request, 'qmeet/createevent.html')


def new_event(request):
    #if request.method == 'POST':
    #    try:
            event_name = request.POST['event-name']
            start_date = request.POST['start-date']
            end_date = request.POST['end-date']
            capacity = request.POST['capacity']
            #event_image = request.POST['event-image']
            event = Event(title=event_name, start_date=start_date, end_date=end_date, capacity=capacity)#, image=event_image)
            event.save()
            return render(request, 'index.html')
    #    except:
    #        return HttpResponse("Event failed to create")


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
    students = Student.objects.all().values()
    return JsonResponse({
        'students': list(students)
    })


@login_required()
def get_all_events(request):
    events = Event.objects.all().values()
    # serializer = EventSerializer(event)
    # serializer_data = serializer.data
    # json = JSONRenderer().render(serializer_data).decode()
    return JsonResponse({
        'events': list(events)
    })
