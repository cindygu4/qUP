from django.db import models
from apps.teachers.models import Classroom, Queue

# Create your models here.
class Notification(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='notifications')
    content = models.CharField(max_length=64)

class Feedback(models.Model):
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )

    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
