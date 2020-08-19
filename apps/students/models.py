from django.db import models
from apps.teachers.models import Classroom, Queue
from apps.users.models import Student
from django.utils import timezone

# Create your models here.
class Notification(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='notifications')
    content = models.CharField(max_length=64)
    date = models.DateField(blank=False, null=True)
    time = models.TimeField(blank=False, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "queue_name": self.queue.name,
            "class_name": self.queue.classroom.name,
            "date": self.date.strftime("%b %-d %Y"),
            "time": self.time.strftime("%-I:%M %p"),
            "content": self.content
        }

class OfficeHoursLine(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='oh_lines')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='oh_lines')
    got_help = models.BooleanField(default=False)
    time_joined = models.TimeField(blank=False, null=True)

'''If a student was in the line and got help, then create a feedback form for them to fill out.'''
class Feedback(models.Model):
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )

    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='ratings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ratings', null=True)
    completed = models.BooleanField(default=False)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
