from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

USER_CHOICES = (
    ("Student", "Student"),
    ("Instructor", "Instructor")
)

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=USER_CHOICES, label="I am a:")\

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "user_type", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if self.cleaned_data["user_type"] == "Instructor":
            user.is_teacher = True
        else:
            user.is_student = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address already taken. Try again.')
        return email