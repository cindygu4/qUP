from django import forms

class JoinClassForm(forms.Form):
    class_code = forms.CharField(max_length=7, min_length=7, label="Classroom Code")

class JoinQueueForm(forms.Form):
    location = forms.CharField(max_length=100, label="Location (If online office hours, please put Online.)")
    meeting_url = forms.URLField(max_length=100, required=False, label="Meeting URL")
    description = forms.CharField(required=False, max_length=280, label="Description",
                                  widget=forms.Textarea(attrs={
                                      'placeholder': 'Add description of what you need help on'}))
