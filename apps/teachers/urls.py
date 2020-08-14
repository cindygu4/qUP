from django.urls import path

from . import views

app_name = "teachers"

urlpatterns = [
    path('', views.index, name='index'),
    path('classes/', views.view_classes, name='view_classes'),
    path('classes/add/', views.add_class, name='add_class')
]
