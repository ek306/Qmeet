from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Subquery
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from rest_framework import generics
from . import serializers
from .forms import StudentCreationForm, StudentCategoriesForm, EventCategoriesForm, FilterStudentsForm, FilterEventsForm
from .models import Student, Event, StudentProfile, StudentCategories, StudentEvents, EventCategories, \
    StudentProfileYear, FriendRequest, Categories
from django.views.generic import CreateView


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
    user = request.user
    form = StudentCategoriesForm()
    try:
        user_sp = get_profile_by_student(user)
        context = {'profile': user_sp, 'form': form}
        return render(request, 'qmeet/createstudentprofile.html', context)

    except StudentProfile.DoesNotExist:
        context = {'profile': None, 'form': form}
        return render(request, 'qmeet/createstudentprofile.html', context)


@login_required()
def new_student_profile(request):
    user = request.user
    if request.method == 'POST':
        form = StudentCategoriesForm(request.POST)
        if form.is_valid():
            student = user
            bio = request.POST['bio']
            location = form.cleaned_data['location']
            course = form.cleaned_data['course']
            year = form.cleaned_data['year']
            # display_picture = form.cleaned_data['display_picture']

            try:
                student_profile = get_profile_by_student(user)
                StudentProfile.objects.filter(student=student).update(student=student, course=course, bio=bio, location=location)
                StudentCategories.objects.filter(student_profile=student_profile).delete()

            except StudentProfile.DoesNotExist:
                student_profile = StudentProfile(student=student, course=course, bio=bio, location=location)  # , display_picture=display_picture)
                student_profile.save()

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


@method_decorator(login_required, name='dispatch')
class CreateEventView(CreateView):
    template_name = 'qmeet/createevent.html'
    form_class = EventCategoriesForm


# def createevent(request):
#    form = EventCategoriesForm()
#    return render(request, 'qmeet/createevent.html', {'form': form})


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
            event.attendees.add(user)
            student_event = StudentEvents(student=user, event=event)
            student_event.save()

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
            title = request.POST['title']
            location = request.POST['location']
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
    form = FilterStudentsForm()
    return render(request, 'qmeet/students.html', {'form': form})


@login_required()
def events(request):
    form = FilterEventsForm()
    return render(request, 'qmeet/events.html', {'form': form})


class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer


@login_required()
def get_friend_list(request):
    user = request.user
    cursor = connection.cursor()
    cursor.execute('call GetFriendsSP(' + str(user.id) + ')')
    filtered_users = cursor.fetchall()
    return JsonResponse({
        'students': list(filtered_users)
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def reject_friend_request(request):
    to_user = request.user
    from_user_id = request.GET['student_id']
    from_user = get_student_by_id(from_user_id)
    frequest = FriendRequest.objects.get(to_user=to_user, from_user=from_user)
    frequest.delete()
    return HttpResponse("Successfully rejected the request!")


@login_required()
def remove_friend(request):
    user = request.user
    sp_id = request.GET['student_profile_id']
    student_profile = StudentProfile.objects.get(id=sp_id)
    user_student_profile = get_profile_by_student(user)
    user_student_profile.friends.remove(student_profile)
    student_profile.friends.remove(user_student_profile)
    return HttpResponse("Removed from friend list")


@login_required()
def compare_user_and_student_profile(request):
    user = request.user
    sp_id = request.GET['student_profile_id']
    student_profile = StudentProfile.objects.get(id=sp_id)
    user_profile = StudentProfile.objects.get(student=user)
    if student_profile == user_profile:
        return JsonResponse({
            'context': "Same"
        })
    else:
        is_friends_empty = student_profile.friends
        if is_friends_empty.exists():
            for friend in student_profile.friends.all():
                if user_profile == friend:
                    return JsonResponse({
                        'context': "Friends"
                    })
                else:
                    return JsonResponse({
                        'context': "Neither"
                    })
        else:
            return JsonResponse({
                'context': "Neither"
            })


@login_required()
def join_event(request):
    user = request.user
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    event.attendees.add(user)
    student_event = StudentEvents(student=user, event=event)
    student_event.save()
    return HttpResponse("You have joined the event!")


@login_required()
def leave_event(request):
    user = request.user
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    event.attendees.remove(user)
    student_event = StudentEvents.objects.get(student=user, event=event)
    student_event.delete()
    return HttpResponse("You have left the event")


@login_required()
def get_student_categories(request):
    sp_id = request.GET['student_profile_id']
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
def check_user_is_host(request):
    user = request.user
    user_sp = get_profile_by_student(user)
    student_profile_id = request.GET.get('event_host_spid')
    student_profile = StudentProfile.objects.get(id=student_profile_id)
    event_id = request.GET.get('event_id')
    event = Event.objects.get(id=event_id)
    if user_sp == student_profile:
        return JsonResponse({
            'context': "Host"
        })
    else:
        student_events = StudentEvents.objects.filter(event=event)
        if student_events.exists():
            for student_event in student_events:
                if student_event.student == user:
                    return JsonResponse({
                        'context': "Attendee"
                    })
            else:
                return JsonResponse({
                    'context': "Neither"
                })
        else:
            return JsonResponse({
                'context': "Neither"
            })


def get_hosted_events(request):
    user = request.user
    events = Event.objects.filter(host=user).values()
    return JsonResponse({
        'hosted_events': list(events)
    })


def filter_student(request):
    if request.method == "POST":
        form = FilterStudentsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            categories_list = []
            categories = form.cleaned_data['categories']
            for category in categories:
                categories_list.append(category.category)

            categories_string = ','.join(categories_list)
            cursor = connection.cursor()
            cursor.execute('call FilterSP(' + '"' + str(username) + '"' + ', ' + '"' + categories_string + '"' + ')')
            filtered_users = cursor.fetchall()
            return JsonResponse({'filtered_users': filtered_users})


@login_required()
def filter_events(request):
    if request.method == "POST":
        form = FilterEventsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            categories_list = []
            categories = form.cleaned_data['categories']
            for category in categories:
                categories_list.append(category.category)

            categories_string = ','.join(categories_list)
            cursor = connection.cursor()
            cursor.execute('call FilterEventSP(' + '"' + str(title) + '"' + ', ' + '"' + categories_string + '"' + ')')
            filtered_events = cursor.fetchall()
            return JsonResponse({'filtered_events': filtered_events})


@login_required()
def get_joined_events(request):
    user = request.user
    student_events = StudentEvents.objects.filter(student=user).exclude(event__host=user)
    if student_events.exists():
        joined_events = Event.objects.filter(id__in=Subquery(student_events.values('event_id'))).values()
        return JsonResponse({
            'joined_events': list(joined_events)
        })
    else:
        return JsonResponse({
            'joined_events': None
        })


@login_required()
def get_timetable(request):
    cursor = connection.cursor()
    cursor.execute('call GetTimetableForUserSP(' + str(request.user.id) + ')')
    semester_module = cursor.fetchall()
    return JsonResponse({'GetTimetableForUser': semester_module})


@login_required()
def timetable(request):
    return render(request, 'qmeet/timetable.html')
