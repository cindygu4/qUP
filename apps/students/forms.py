from django import forms

class JoinClassForm(forms.Form):
    class_code = forms.CharField(max_length=7, min_length=7, label="Classroom Code")