from django.urls import path

from . import views

app_name = "teachers"

urlpatterns = [
    path('', views.index, name='index'),
    path('classes/', views.view_classes, name='view_classes'),
    path('classes/add/', views.add_class, name='add_class'),
    path('classes/<int:class_id>', views.view_class, name='view_class'),
    path('upcoming/', views.upcoming_oh, name='upcoming_oh'),
    path('classes/<int:class_id>/queues/add', views.add_queue, name='add_queue')
]
