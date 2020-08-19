from django.urls import path

from . import views

app_name = "teachers"

urlpatterns = [
    path('', views.index, name='index'),
    path('classes/', views.view_classes, name='view_classes'),
    path('classes/add/', views.add_class, name='add_class'),
    path('classes/<int:class_id>/', views.view_class, name='view_class'),
    path('classes/<int:class_id>/delete/', views.delete_class, name='delete_class'),
    path('upcoming/', views.upcoming_oh, name='upcoming_oh'),
    path('classes/<int:class_id>/queues/add/', views.add_queue, name='add_queue'),
    path('queues/<int:queue_id>/open/', views.open_queue, name='open_queue'),
    path('queues/<int:queue_id>/opened/', views.opened_queue, name='opened_queue'),
    path('queues/<int:queue_id>/delete/', views.delete_queue, name='delete_queue'),
    path('queues/<int:queue_id>/edit/', views.edit_queue, name='edit_queue'),
    path('queues/<int:line_id>/done/', views.finished_helping, name='finished_helping'),
    path('queues/<int:queue_id>/end/', views.end_queue, name='end_queue'),

    # API stuff
    path('classes/<int:class_id>/rename_class/', views.edit_class_name, name='rename_class')
]
