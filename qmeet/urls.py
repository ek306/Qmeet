from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('studentprofile/', views.studentprofile, name='create student profile'),
    path('new_student_profile', views.new_student_profile, name='new student profile'),
    path('createevent/', views.CreateEventView.as_view(), name='create event'),
    path('updateevent/', views.updateevent, name='update event page'),
    path('new_event', views.new_event, name="new event"),
    path('update_event', views.update_event, name='update event'),
    path('students/', views.students, name="students"),
    path('events/', views.events, name="events"),
#    path('allstudents/', views.StudentListView.as_view()),
#    path('allevents/', views.EventListView.as_view()),
    path('get_friend_list', views.get_friend_list, name="get friend list"),
    path('get_all_events', views.get_all_events, name="get all events"),
    path('getevent/', views.get_event, name='get event'),
    path('getstudentprofile/', views.get_student_profile, name='get student profile'),
    path('get_hosted_events', views.get_hosted_events, name='get hosted events'),
    path('send_friend_request', views.send_friend_request, name='send friend request'),
    path('cancel_friend_request', views.cancel_friend_request, name='cancel friend request'),
    path('get_friend_requests', views.get_friend_requests, name='get friend requests'),
    path('get_sent_friend_requests', views.get_sent_friend_requests, name='get sent friend requests'),
    path('accept_friend_request', views.accept_friend_request, name='accept friend request'),
    path('reject_friend_request', views.reject_friend_request, name='reject friend request'),
    path('remove_friend', views.remove_friend, name='remove friend'),
    path('join_event', views.join_event, name='join event'),
    path('leave_event', views.leave_event, name='leave event'),
    path('get_student_categories', views.get_student_categories, name='get student categories'),
    path('compare_user_and_student_profile', views.compare_user_and_student_profile, name='compare user and student profile'),
    path('check_student_profile_exists', views.check_student_profile_exists, name='check student profile exists'),
    path('check_user_is_host', views.check_user_is_host, name='check user is host'),
    path('filter_student', views.filter_student, name='filter students'),
    path('filter_events', views.filter_events, name='filter events'),
    path('get_joined_events', views.get_joined_events, name='get joined events'),
    path('get_recommended_events', views.get_recommended_events, name='get recommended events'),
    path('timetable/', views.timetable, name='timetable'),
    path('get_student_timetable', views.get_student_timetable, name="get student timetable"),
    path('get_unread_messages', views.get_unread_messages, name="get unread messages"),
    path('render_student_profile', views.render_student_profile, name="render student profile")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT, }),
    ]