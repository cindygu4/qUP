from django.db import models
from apps.users.models import Teacher, Student

# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=64)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrooms')
    students = models.ManyToManyField(Student, related_name='classrooms')
    code = models.CharField(max_length=7, blank=False, unique=True)

class Queue(models.Model):
    name = models.CharField(max_length=64)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='queues')
    date = models.DateField(blank=False)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    location = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    opened = models.BooleanField(default=False)
    currently_meeting = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    meeting_url = models.URLField(max_length=100, null=True, blank=True)
    has_meeting_url = models.BooleanField(default=False)
