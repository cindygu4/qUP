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
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    frequency = models.CharField(max_length=7, blank=False)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
