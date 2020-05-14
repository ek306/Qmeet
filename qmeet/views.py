from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Subquery
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentCreationForm, StudentCategoriesForm, EventCategoriesForm
from .models import Student, Event, StudentProfile, StudentCategories, EventCategories, StudentProfileYear, FriendRequest, Categories
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from . import serializers
from .models import Student, Event, StudentProfile, StudentCategories, EventCategories, StudentProfileYear


class Timetable:

    def __init__(self):
        self.semester_modules = []

    def add_module(self, module):
        self.semester_modules.append(module)


class SemesterModule:

    def __init__(self, semester_name, module_name, start_time, end_time, academic_year, day_of_week):
        self.semester_name = semester_name
        self.module_name = module_name
        self.day_of_week = day_of_week
        self.module_start_time = start_time
        self.module_end_time = end_time
        self.academic_year = academic_year


class SignUp(generic.CreateView):
    form_class = StudentCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def get_profile_by_student(student):
    sp = StudentProfile.objects.get(student=student)
    return sp


def get_student_by_id(id):
    student = Student.objects.get(id=id)
    return student


@login_required()
def studentprofile(request):
    form = StudentCategoriesForm()
    return render(request, 'qmeet/createstudentprofile.html', {'form': form})


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
            student_profile = get_profile_by_student(user)

            if student_profile is None:
                student_profile = StudentProfile(student=student, course=course, bio=bio, location=location)  # , display_picture=display_picture)
                student_profile.save()
            else:
                StudentProfile.objects.filter(student=student).update(student=student, course=course, bio=bio, location=location)
                StudentCategories.objects.filter(student_profile=student_profile).delete()

            for categories in form.cleaned_data['categories']:
                student_categories = StudentCategories(student_profile=student_profile, categories=categories)
                student_categories.save()

            student_profile_year = StudentProfileYear.objects.filter(student_profile=student_profile, year=year)
            if not student_profile_year:
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


@login_required()
def updateevent(request):
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    form = EventCategoriesForm()
    context = {'event': event, 'form': form}
    return render(request, 'qmeet/updateevent.html', context)


def new_event(request):
    user = request.user
    if request.method == "POST":
        form = EventCategoriesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            location = form.cleaned_data['location']
            start_date = request.POST['start-date']
            end_date = request.POST['end-date']
            capacity = form.cleaned_data['capacity']
            event = Event(host=user, title=title, location=location, start_date=start_date, end_date=end_date, capacity=capacity)
            event.save()

            for categories in form.cleaned_data['categories']:
                event_categories = EventCategories(event=event, categories=categories)
                event_categories.save()
            return HttpResponse("Event created, and event categories created")


def update_event(request):
    user = request.user
    if request.method == "POST":
        form = EventCategoriesForm(request.POST)
        if form.is_valid():
            event_id = request.GET['event_id']
            event = Event.objects.get(id=event_id)
            title = form.cleaned_data['title']
            location = form.cleaned_data['location']
            start_date = request.POST['start-date']
            end_date = request.POST['end-date']
            capacity = form.cleaned_data['capacity']
            EventCategories.objects.filter(event=event).delete()
            Event.objects.filter(id=event_id).update(host=user, title=title, location=location, start_date=start_date, end_date=end_date, capacity=capacity)

            for categories in form.cleaned_data['categories']:
                event_categories = EventCategories(event=event, categories=categories)
                event_categories.save()
            return HttpResponse("Event updated, and event categories created")


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
    student = get_student_by_id(student_id)
    student_profile = get_profile_by_student(student)
    user = request.user
    user_sp = get_profile_by_student(user)
    context = {
        'student_profile': student_profile,
        'user_profile': user_sp
    }
    return render(request, 'qmeet/getstudentprofile.html', context)


@login_required()
def send_friend_request(request):
    from_user = request.user
    student_id = request.GET['student_id']
    to_user = get_student_by_id(student_id)
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
    to_user = get_student_by_id(to_user_id)
    frequest = FriendRequest.objects.get(to_user=to_user, from_user=from_user)
    frequest.delete()
    return HttpResponse("Successfully cancelled friend request!")


@login_required()
def accept_friend_request(request):
    to_user = request.user
    to_user_sp = get_profile_by_student(to_user)
    from_user_id = request.GET['student_id']
    from_user = get_student_by_id(from_user_id)
    from_user_sp = get_profile_by_student(from_user)
    to_user_sp.friends.add(from_user_sp)
    from_user_sp.friends.add(to_user_sp)
    frequest = FriendRequest.objects.get(to_user=to_user, from_user=from_user)
    frequest.delete()
    return HttpResponse("Successfully accepted the request!")


@login_required()
def reject_friend_request(request):
    to_user = request.user
    from_user_id = request.GET['student_id']
    from_user = get_student_by_id(from_user_id)
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


@login_required()
def get_student_categories(request):
    sp_id = request.GET['student_profile_id']
    #student_profile = StudentProfile.objects.get(id=sp_id)
    categories_f = StudentCategories.objects.filter(student_profile_id=sp_id).values()
    categories = Categories.objects.filter(id__in=Subquery(categories_f.values('categories_id'))).values()
    return JsonResponse({
        'categories': list(categories)
    })


@login_required()
def check_student_profile_exists(request):
    user = request.user
    try:
        user_sp = get_profile_by_student(user)
        return JsonResponse({
            'profile_exists': True
        })
    except StudentProfile.DoesNotExist:
        return JsonResponse({
            'profile_exists': False
        })


@login_required()
def compare_profiles(request):
    user = request.user
    user_sp = get_profile_by_student(user)
    student_profile_id = request.GET['student_profile_id']
    student_profile = StudentProfile.objects.get(id=student_profile_id)
    if user_sp == student_profile:
        return JsonResponse({
            'context': True
        })
    else:
        return JsonResponse({
            'context': False
        })


def get_hosted_events(request):
    user = request.user
    events = Event.objects.filter(host=user).values()
    return JsonResponse({
        'hosted_events': list(events)
    })


@login_required()
def get_timetable(request):
    timetable = Timetable()
    semester_module = SemesterModule("S1", "Introduction to Python", 9, 11, 2019, "Monday")
    timetable.add_module(semester_module)
    semester_module = SemesterModule("S1", "Operating Systems", 11, 12, 2019, "Wednesday")
    timetable.add_module(semester_module)
    semester_module = SemesterModule("S1", "Introduction to Python (Lab)", 14, 15, 2019, "Monday")
    timetable.add_module(semester_module)
    semester_module = SemesterModule("S1", "Databases 101", 14, 16, 2019, "Thursday")
    timetable.add_module(semester_module)
    semester_module = SemesterModule("S1", "Databases 101 (Lab)", 13, 14, 2019, "Friday")
    timetable.add_module(semester_module)
    context = {'timetable': timetable}
    return render(request, 'qmeet/timetable.html', context)


