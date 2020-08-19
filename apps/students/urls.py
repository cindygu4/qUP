from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path('', views.index, name='index'),
    path('classes/', views.view_classes, name='view_classes'),
    path('classes/join/', views.join_class, name='join_class'),
    path('upcoming/', views.upcoming_oh, name='upcoming_oh'),
    path('my_notifications/', views.view_notifications, name='view_notifications'),
    path('queues/<int:queue_id>/opened/', views.opened_queue, name='opened_queue'),
    path('queues/<int:queue_id>/join/', views.join_queue, name='join_queue'),
    path('queues/<int:queue_id>/give_feedback/', views.give_feedback, name='give_feedback'),

    # API stuff
    path('notifications/', views.notifications, name='notifications_api')
]
