from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Subquery
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentCreationForm, StudentCategoriesForm, EventCategoriesForm
from .models import Student, Event, StudentProfile, StudentCategories, EventCategories, StudentProfileYear, FriendRequest
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from . import serializers
from django.views.decorators.csrf import ensure_csrf_cookie


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
    user = request.user
    students_f = StudentProfile.objects.exclude(student=user)
    student_list = Student.objects.filter(id__in=Subquery(students_f.values('student_id'))).values()
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
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'qmeet/getevent.html', context)


@login_required()
def get_student_profile(request):
    student_id = request.GET['student_id']
    student = Student.objects.get(id=student_id)
    student_profile = StudentProfile.objects.get(student=student)
    context = {'student_profile': student_profile}
    return render(request, 'qmeet/getstudentprofile.html', context)

@login_required()
def send_friend_request(request):
    from_user = request.user
    student_id = request.GET['student_id']
    to_user = Student.objects.get(id=student_id)
    new_request, created = FriendRequest.objects.get_or_create(to_user=to_user, from_user=from_user)
    return HttpResponse("Friend request object created")


@login_required()
def get_friend_requests(request):
    user = request.user
    friend_requests_f = FriendRequest.objects.filter(to_user=user).values()
    received_friend_requests = Student.objects.filter(id__in=Subquery(friend_requests_f.values('from_user_id'))).values()
    return JsonResponse({
        "friend_requests": list(received_friend_requests)
    })


@login_required()
def get_sent_friend_requests(request):
    user = request.user
    friend_requests_f = FriendRequest.objects.filter(from_user=user).values()
    sent_friend_requests = Student.objects.filter(id__in=Subquery(friend_requests_f.values('to_user_id'))).values()
    return JsonResponse({
        "sent_requests": list(sent_friend_requests)
    })


@login_required()
def cancel_friend_request(request):
    from_user = request.user
    to_user_id = request.GET['student_id']
    to_user = Student.objects.get(id=to_user_id)
    frequest = FriendRequest.objects.get(to_user=to_user, from_user=from_user)
    frequest.delete()
    return HttpResponse("Successfully cancelled friend request!")

@login_required()
def accept_friend_request(request):
    to_user = request.user
    to_user_sp = StudentProfile.objects.get(student=to_user)
    from_user_id = request.GET['student_id']
    from_user = Student.objects.get(id=from_user_id)
    from_user_sp = StudentProfile.objects.get(student=from_user)
    to_user_sp.friends.add(from_user_sp)
    from_user_sp.friends.add(to_user_sp)
    frequest = FriendRequest.objects.get(to_user=to_user, from_user=from_user)
    frequest.delete()
    return HttpResponse("Successfully accepted the request!")


@login_required()
def reject_friend_request(request):
    to_user = request.user
    from_user_id = request.GET['student_id']
    from_user = Student.objects.get(id=from_user_id)
    frequest = FriendRequest.objects.get(to_user=to_user, from_user=from_user)
    frequest.delete()
    return HttpResponse("Successfully rejected the request!")


@login_required()
def join_event(request):
    user = request.user
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    for t in event.attendees.all():
        if t == user:
            return HttpResponse("Already joined!")

    event.attendees.add(user)
    return HttpResponse("You have joined the event!")
