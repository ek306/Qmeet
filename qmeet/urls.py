from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('studentprofile/', views.studentprofile, name='student profile'),
    path('new_student_profile', views.new_student_profile, name='new student profile'),
    path('createevent/', views.createevent, name='create event'),
    path('new_event', views.new_event, name="new event"),
    path('students/', views.students, name="students"),
    path('events/', views.events, name="events"),
    path('allstudents/', views.StudentListView.as_view()),
    path('allevents/', views.EventListView.as_view()),
    path('get_all_students', views.get_all_students, name="get all students"),
    path('get_all_events', views.get_all_events, name="get all events"),
    path('getevent/', views.get_event, name='get event'),
    path('getstudentprofile/', views.get_student_profile, name='get student profile'),
    path('send_friend_request', views.send_friend_request, name='send friend request'),
    path('cancel_friend_request', views.cancel_friend_request, name='cancel friend request'),
    path('get_friend_requests', views.get_friend_requests, name='get friend requests'),
    path('get_sent_friend_requests', views.get_sent_friend_requests, name='get sent friend requests'),
    path('accept_friend_request', views.accept_friend_request, name='accept friend request'),
    path('reject_friend_request', views.reject_friend_request, name='reject friend request'),
    path('join_event', views.join_event, name='join event'),

]