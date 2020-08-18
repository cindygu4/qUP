from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import JoinClassForm
from apps.teachers.models import Classroom, Queue
from apps.users.models import Teacher, Student
from django.contrib import messages

# Create your views here.
def is_student(user):
    return user.is_student

@login_required
@user_passes_test(is_student)
def index(request):
    return render(request, "students/index.html")

@login_required
@user_passes_test(is_student)
def join_class(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            class_code = form.cleaned_data['class_code']
            if Classroom.objects.filter(code=class_code).exists():
                classroom = Classroom.objects.get(code=class_code)
                student = Student.objects.get(user=request.user)
                student.classrooms.add(classroom)
                return redirect('students:view_classes')
            else:
                messages.error(request, "No classrooms match this code. Try again.")
    else:
        form = JoinClassForm()

    return render(request, "students/join_class.html", {
        'form': form
    })

@login_required
@user_passes_test(is_student)
def view_classes(request):
    classrooms = Classroom.objects.filter(students__user=request.user)
    return render(request, "students/classes.html", {
        'classrooms': classrooms
    })

@login_required
@user_passes_test(is_student)
def upcoming_oh(request):
    # order the teacher's queues by date then start time
    queues = Queue.objects.filter(classroom__students__user=request.user).order_by('date', 'start_time')\
        .exclude(opened=True)
    return render(request, "students/upcoming_oh.html", {
        'queues': queues
    })