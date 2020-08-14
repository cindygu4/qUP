from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path('', views.index, name='index'),
    path('classes/', views.view_classes, name='view_classes'),
    path('classes/join', views.join_class, name='join_class')
]
