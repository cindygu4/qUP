from django import forms
from .models import Classroom, Queue

class NewClassroomForm(forms.Form):
    name = forms.CharField(max_length=64, label="Class Name")