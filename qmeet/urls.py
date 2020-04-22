from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('createevent/', views.createevent, name='create event'),
    path('new_event', views.new_event, name="new event"),
    path('students/', views.students, name="students"),
    path('events/', views.events, name="events"),
    path('allstudents/', views.StudentListView.as_view()),
    path('allevents/', views.EventListView.as_view()),
    path('get_all_students', views.get_all_students, name="get all students"),
    path('get_all_events', views.get_all_events, name="get all events"),
]