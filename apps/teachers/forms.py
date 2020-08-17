from django import forms
from django.core.exceptions import ValidationError
from .models import Classroom, Queue
import datetime

DAY_CHOICES = (
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
    ('7', 'Sunday')
)

def validate_date(date):
    if date < datetime.date.today():
        raise ValidationError(u'Date must be today or later')

class NewClassroomForm(forms.Form):
    name = forms.CharField(max_length=64, label="Class Name")

class NewQueueForm(forms.Form):
    name = forms.CharField(max_length=64, label="Office Hours Name")
    date = forms.DateField(validators=[validate_date], label="Date",
                           widget=forms.widgets.DateInput(attrs={'type': 'date', 'placeholder': 'mm/dd/yyyy'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'placeholder': 'hh:mm --'}),
                                 label="Start Time (Please specify AM or PM.)")
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'placeholder': 'hh:mm --'}),
                               label="End Time (Please specify AM or PM.)")
    location = forms.CharField(max_length=100, label="Location (If online office hours, please put Online.)")
    meeting_url = forms.URLField(max_length=100, required=False, label="Meeting URL")
    description = forms.CharField(required=False, max_length=280, label="Additional Information",
                                  widget=forms.Textarea(attrs={
                                      'placeholder': 'Add optional description or any other information here'}))