from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Classroom, Queue
from apps.users.models import Teacher
from .forms import NewClassroomForm

# Create your views here.
def is_teacher(user):
    return user.is_teacher

@login_required
@user_passes_test(is_teacher)
def index(request):
    return render(request, "teachers/index.html")

@login_required
@user_passes_test(is_teacher)
def view_classes(request):
    teacher = request.user.teacher_profile
    classes = Classroom.objects.filter(teacher=teacher)
    return render(request, "teachers/classes.html", {
        'classes': classes
    })

@login_required
@user_passes_test(is_teacher)
def add_class(request):
    if request.method == 'POST':
        form = NewClassroomForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data['name']
            Classroom.objects.create(name=class_name, teacher=request.user.teacher_profile)
            return redirect('teachers:view_classes')
    else:
        form = NewClassroomForm()
    return render(request, "teachers/add_class.html", {
        'form': form
    })
