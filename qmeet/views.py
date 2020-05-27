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


class SignUp(generic.CreateView):
    """
    Simple form view which creates a
    student object
    """
    form_class = StudentCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def get_profile_by_student(student):
    """
    Given a student object parameter
    retrieve the student profile associated
    with that student
    """
    sp = StudentProfile.objects.get(student=student)
    return sp


def get_student_by_id(id):
    """
    Given an student ID retrieve the student
    object associated with that ID
    """
    student = Student.objects.get(id=id)
    return student


@login_required()
def studentprofile(request):
    """
    Renders an empty create student profile form if
    student profile does not exists, and returns
    student profile form with filled in details if
    student profile exists
    """
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
    """
    Creates student profile using form inputs if student profile does not exist,
    and updates student profile if student profile exists

    Populates StudentCategories table with the student profile and
    categories that they have selected in the form, replacing any
    existing relations with that student profile
    """
    user = request.user
    if request.method == 'POST':
        form = StudentCategoriesForm(request.POST, request.FILES)
        if form.is_valid():
            student = user
            bio = request.POST['bio']
            location = form.cleaned_data['location']
            course = form.cleaned_data['course']
            year = form.cleaned_data['year']
            display_picture = request.FILES.get('display_picture')

            try:
                student_profile = get_profile_by_student(user)
                StudentProfile.objects.filter(student=student).update \
                        (
                        student=student, course=course, bio=bio, location=location, display_picture=display_picture
                    )
                StudentCategories.objects.filter(student_profile=student_profile).delete()

            except StudentProfile.DoesNotExist:
                student_profile = StudentProfile(
                    student=student, course=course, bio=bio, location=location, display_picture=display_picture
                )
                student_profile.save()

            for categories in form.cleaned_data['categories']:
                student_categories = StudentCategories(student_profile=student_profile, categories=categories)
                student_categories.save()

            student_profile_year = StudentProfileYear.objects.filter(student_profile=student_profile, year=year)
            if not student_profile_year:
                student_profile_year = StudentProfileYear(student_profile=student_profile, year=year)
                student_profile_year.save()
            return HttpResponseRedirect("/qmeet")


@login_required()
def index(request):
    """
    Renders index.html, which is a dashboard for the student
    """
    return render(request, 'index.html')


@method_decorator(login_required, name='dispatch')
class CreateEventView(CreateView):
    """
    Renders createevent.html with create event form with bootstrap formatting
    """
    template_name = 'qmeet/createevent.html'
    form_class = EventCategoriesForm


# def createevent(request):
#    form = EventCategoriesForm()
#    return render(request, 'qmeet/createevent.html', {'form': form})


@login_required()
def updateevent(request):
    """
    Renders updatevent.html with the same form used for creating an event
    """
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    form = EventCategoriesForm()
    context = {'event': event, 'form': form}
    return render(request, 'qmeet/updateevent.html', context)


def new_event(request):
    """
    Creates an event where the user is the host, adds the user to the list of attendees
    and populates the StudentEvent table with the user and the event

    Populates EventCategories table with the event and the categories selected
    in the form, then redirects to index.html
    """
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
            return HttpResponseRedirect('/qmeet')


def update_event(request):
    """
    Updates event and replaces EventCategories objects (with the old event) with new objects

    Redirects to index.html on success
    """
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
            return HttpResponseRedirect('/qmeet')


@login_required()
def students(request):
    """
    Renders a form which allows students to search for student profiles by
    username or category interests
    """
    form = FilterStudentsForm()
    return render(request, 'qmeet/students.html', {'form': form})


@login_required()
def events(request):
    """
    Renders a form which allows students to search for events by
    username or category interests
    """
    form = FilterEventsForm()
    return render(request, 'qmeet/events.html', {'form': form})

@login_required()
class StudentListView(generics.ListAPIView):
    """
    Renders a view that shows all students in a query set form
    using Django's rest framework, useful for understanding queryset nature

    Produced as test for practise and learning, not used in application
    """
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class EventListView(generics.ListAPIView):
    """
    Renders a view that shows all events in a query set form
    using Django's rest framework,

    Produced as test for practise and learning, not used in application
    """
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer


@login_required()
def get_friend_list(request):
    """
    Uses GetFriendsSP stored procedure to run SQL code that
    retrieves all of the users friends and returns the list
    of friends as a JsonResponse to be rendered dynamically
    on the HTML
    """
    student_id = request.GET.get('student_id')
    cursor = connection.cursor()
    cursor.execute('call GetFriendsSP(' + str(student_id) + ')')
    filtered_users = cursor.fetchall()
    return JsonResponse({
        'students': list(filtered_users)
    })


@login_required()
def get_all_events(request):
    """
    Returns a list of all events in the database that have been created
    """
    event_list = Event.objects.all().values()
    return JsonResponse({
        'events': list(event_list)
    })


@login_required()
def get_event(request):
    """
    Gets details of an event from the database and returns the data as
    JsonResponse to be rendered dynamically on the HTML
    """
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    event_categories = EventCategories.objects.filter(event=event) \
        .select_related('categories').values_list('categories__category')

    context = {'event': event, 'categories': event_categories}
    return render(request, 'qmeet/getevent.html', context)


@login_required()
def get_student_profile(request):
    """
    Gets details of a student profile and the current student logged in

    Context is then used to render data on the HTML using Django templates,
    as well as passing data back to views in various AJAX requests
    """
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
    """
    Creates an instance of FriendRequest where the user sending the friend request
    is the sender and the user receiving the friend request is the receiver
    """
    from_user = request.user
    student_id = request.GET['student_id']
    to_user = get_student_by_id(student_id)
    new_request, created = FriendRequest.objects.get_or_create(to_user=to_user, from_user=from_user)
    return redirect('index')
    #return HttpResponse("Friend request object created")


@login_required()
def get_friend_requests(request):
    """
    Returns all friend request objects where the user is the to_user (receiver)
    """
    user = request.user
    friend_requests_f = FriendRequest.objects.filter(to_user=user).values()
    received_friend_requests = Student.objects.filter(id__in=Subquery(friend_requests_f.values('from_user_id'))).values()
    return JsonResponse({
        "friend_requests": list(received_friend_requests)
    })


@login_required()
def get_sent_friend_requests(request):
    """
    Returns all friend request objects where the user is the sender
    """
    user = request.user
    friend_requests_f = FriendRequest.objects.filter(from_user=user).values()
    sent_friend_requests = Student.objects.filter(id__in=Subquery(friend_requests_f.values('to_user_id'))).values()
    return JsonResponse({
        "sent_requests": list(sent_friend_requests)
    })


@login_required()
def cancel_friend_request(request):
    """
    Cancels a sent friend request by deleting the FriendRequest object as
    the sender
    """
    from_user = request.user
    to_user_id = request.GET['student_id']
    to_user = get_student_by_id(to_user_id)
    frequest = FriendRequest.objects.get(to_user=to_user, from_user=from_user)
    frequest.delete()
    return redirect('index')


@login_required()
def accept_friend_request(request):
    """
    Adds the sender to the receiver's friend list and vice versa, then
    deletes the FriendRequest object
    """
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
    """
    Rejects the friend request by deleting the FriendRequest object as
    the receiver
    """
    to_user = request.user
    from_user_id = request.GET['student_id']
    from_user = get_student_by_id(from_user_id)
    frequest = FriendRequest.objects.get(to_user=to_user, from_user=from_user)
    frequest.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def remove_friend(request):
    """
    Removes a target from the user's friend list and vice versa
    """
    user = request.user
    sp_id = request.GET['student_profile_id']
    student_profile = StudentProfile.objects.get(id=sp_id)
    user_student_profile = get_profile_by_student(user)
    user_student_profile.friends.remove(student_profile)
    student_profile.friends.remove(user_student_profile)
    return redirect('index')


@login_required()
def compare_user_and_student_profile(request):
    """
    On entering a student profile page, determines whether the user's student profile
    and the student profile they are currently viewing is the same, if false checks if
    the student profile is on their friend list

    Returns one of three contexts which is used to render different
    buttons on the HTML when viewing a student profile:
    Update student profile, Add friend or Remove friend
    """
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
    """
    Add user to the list of attendees in the Event table, and creates
    a StudentEvent object
    """
    user = request.user
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    event.attendees.add(user)
    student_event = StudentEvents(student=user, event=event)
    student_event.save()
    return redirect('index')


@login_required()
def leave_event(request):
    """
    Removes user from the list of attendees in the Event table, and deletes
    the StudentEvent object
    """
    user = request.user
    event_id = request.GET['event_id']
    event = Event.objects.get(id=event_id)
    event.attendees.remove(user)
    student_event = StudentEvents.objects.get(student=user, event=event)
    student_event.delete()
    return HttpResponse("You have left the event")


@login_required()
def get_student_categories(request):
    """
    Gets a list of categories that the student is interested in
    """
    sp_id = request.GET['student_profile_id']
    categories_f = StudentCategories.objects.filter(student_profile_id=sp_id).values()
    categories = list(Categories.objects.filter(id__in=Subquery(categories_f.values('categories_id'))).values())
    return JsonResponse({
        'categories': categories
    })


@login_required()
def check_student_profile_exists(request):
    """
    Checks if the current user has created a student profile

    This is used to redirect the user to the view that creates their student profile
    or the view that renders the student profile details when they click on the
    My Profile menu item in the navigation bar
    """
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
    """
    On entering an event page, determines if the current user is the host
    of the event. If false, checks if the user is on the list of attendees
    of the event.

    Returns one of three contexts which is used to render different
    buttons on the HTML when viewing an event:
    Update event, Join event or Leave event
    """
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
    """
    Returns a list of all events that the user is currently the host of
    """
    user = request.user
    events = Event.objects.filter(host=user).values()
    return JsonResponse({
        'hosted_events': list(events)
    })


def filter_student(request):
    """
    Uses a stored procedure FilterSP to run a SQL statement that returns
    a list of students based on user inputs in a form. A user can filter
    students by likeness to a username, categories or both
    """
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
    """
    Uses a stored procedure FilterSP to run a SQL statement that returns
    a list of events based on user inputs in a form. A user can filter
    students by likeness to a title, categories or both
    """
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
    """
    Returns a list of all events where the user is an attendee of the event
    """
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
def get_student_timetable(request):
    """
    Uses a stored procedure GetTimetableForUserSP for the user to view a
    grid formatted timetable based on their course when timetable.html is
    rendered. A student can also view a timetable of a different student.

    For future development, student timetable will be based on individual
    module selection, and will integrate event participation. Courses are currently
    based on SemesterModule objects which are inputted by an admin
    """
    student_id = request.GET.get('student_id')
    cursor = connection.cursor()
    cursor.execute('call GetTimetableForUserSP(' + student_id + ')')
    semester_module = cursor.fetchall()
    return JsonResponse({'GetTimetableForUser': semester_module})


@login_required()
def timetable(request):
    """
    Renders timetable.html and passes the student profile ID
    to the timetable
    """
    student_id = request.GET.get('student_id')
    context = {'student_id': student_id}
    return render(request, 'qmeet/timetable.html', context)


@login_required()
def get_recommended_events(request):
    """
    Uses a stored procedure RecommendedEventsSP to run a SQL statement
    that retrieves a list of events with category selections that match up
    with category selections in the user's student profile
    """
    user = request.user
    user_sp = get_profile_by_student(user)
    categories = StudentCategories.objects.filter(student_profile=user_sp)
    categories_name = Categories.objects.filter(id__in=Subquery(categories.values('categories_id'))).values()
    categories_list = []
    for category in categories_name:
        categories_list.append(category['category'])

    categories_string = ','.join(categories_list)
    cursor = connection.cursor()
    cursor.execute('call RecommendedEventsSP(' + '"' + categories_string + '"' + ')')
    recommended_list = cursor.fetchall()
    return JsonResponse({
        'recommended_events': recommended_list
    })


@login_required()
def get_unread_messages(request):
    """
    Uses a stored procedure GetUnreadMessagesSP to return a count of all messages
    that the user has received but not read. This count also acts as a link to the
    student's inbox
    """
    user = request.user
    cursor = connection.cursor()
    cursor.execute('call GetUnreadMessagesSP(' + '"' + str(user.id) + '"' + ')')
    unread_message_count = cursor.fetchall()
    return JsonResponse({
        'message_count': unread_message_count
    })


@login_required()
def render_student_profile(request):
    user = request.user
    student = request.user
    try:
        user_sp = get_profile_by_student(user)
        student_sp = get_profile_by_student(student)
        context = {
            'student_profile': student_sp,
            'user_profile': user_sp
        }
        return render(request, 'qmeet/getstudentprofile.html', context)

    except StudentProfile.DoesNotExist:
        form = StudentCategoriesForm()
        context = {'form': form}
        return render(request, 'qmeet/createstudentprofile.html', context)

